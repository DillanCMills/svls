############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import asyncio
import time
import uuid
import re
import os
from pathlib import Path
from urllib.parse import unquote, urlparse
from typing import Optional

from pygls.lsp.types.language_features.semantic_tokens import SemanticTokensParams
from .svcpp import *
from pygls.lsp.methods import (COMPLETION, TEXT_DOCUMENT_DID_CHANGE,
                               TEXT_DOCUMENT_DID_CLOSE, TEXT_DOCUMENT_DID_OPEN,
                               TEXT_DOCUMENT_SEMANTIC_TOKENS, 
                               TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL)
from pygls.lsp.types import (CompletionItem, CompletionList, CompletionOptions,
                             CompletionParams, ConfigurationItem,
                             ConfigurationParams, Diagnostic,
                             DidChangeTextDocumentParams,
                             DidCloseTextDocumentParams,
                             DidOpenTextDocumentParams, MessageType, Position,
                             Range, Registration, RegistrationParams,
                             Unregistration, UnregistrationParams, 
                             SemanticTokensOptions,SemanticTokensLegend,
                             SemanticTokens)
from pygls.lsp.types.basic_structures import (DiagnosticSeverity, WorkDoneProgressBegin,
                                              WorkDoneProgressEnd,
                                              WorkDoneProgressReport)
from pygls.server import LanguageServer
from pygls.uris import to_fs_path


COUNT_DOWN_START_IN_SECONDS = 10
COUNT_DOWN_SLEEP_IN_SECONDS = 1

fcomment = re.compile(r'^\s*//')
svfile = re.compile(r'^\s*(.*\.s?vh?)\s*$')
ffile = re.compile(r'^\s*-[fF]\s+(.*\.f)\s*$')
includeFile = re.compile(r'^\s*`include\s+"(.*\.s?vh?)"\s*$')


class SVLanguageServer(LanguageServer):
    CMD_COUNT_DOWN_BLOCKING = 'countDownBlocking'
    CMD_COUNT_DOWN_NON_BLOCKING = 'countDownNonBlocking'
    CMD_PROGRESS = 'progress'
    CMD_REGISTER_COMPLETIONS = 'registerCompletions'
    CMD_SHOW_CONFIGURATION_ASYNC = 'showConfigurationAsync'
    CMD_SHOW_CONFIGURATION_CALLBACK = 'showConfigurationCallback'
    CMD_SHOW_CONFIGURATION_THREAD = 'showConfigurationThread'
    CMD_UNREGISTER_COMPLETIONS = 'unregisterCompletions'

    CONFIGURATION_SECTION = 'svls'

    def __init__(self):
        super().__init__()
        self.files = {}
        self.tempFiles = {}
        self.fileList = []
        self.uvmPkgPath = ''
        self.ignoreUvmPackage = False

        
    def _parse_ffiles(self, files):
        """Parse .f filelist"""

        self.files = {}

        for file in files:
            if file.exists() and not file.is_dir():
                with file.open() as f:
                    for line in f:
                        if fcomment.match(line):
                            continue
                        svf = svfile.match(line)
                        if svf:
                            svf = svf.group(1).replace('$UVM_HOME', self.uvmPkgPath)
                            filePath = (file.parent / Path(svf)).resolve()
                            if filePath.exists() and not filePath.is_dir():
                                # self.fileList.append(filePath)
                                # self.tempFiles[filePath] = None
                                self.files[filePath] = None

        # # Remove deleted files
        # for file in self.files.keys():
        #     if file not in self.tempFiles:
        #         del self.files[file]

        # # Add new files
        # for file in self.tempFiles.keys():
        #     if file not in self.files:
        #         self.files[file] = None

        # self.tempFiles = {}


svls = SVLanguageServer()

async def _validate(ls: SVLanguageServer, params):
    ls.show_message_log('Validating SV...')

    config = await ls.get_configuration_async(
        ConfigurationParams(items=[
            ConfigurationItem(
                scope_uri='',
                section=SVLanguageServer.CONFIGURATION_SECTION
            )
        ])
    )
    # ls.show_message_log(config)

    ffiles = config[0].get('fFileLists')
    svls.ignoreUvmPackage = config[0].get('ignoreUvmPackageWarnings')
    svls.uvmPkgPath = config[0].get('uvmPackagePath')

    if svls.uvmPkgPath == '':
        svls.uvmPkgPath = os.environ.get('UVM_HOME', '')

    # ls.show_message_log(ffiles)

    ffiles = [Path(file.replace('${workspaceRoot}', ls.workspace.root_path)).resolve() for file in ffiles]
    # ls.show_message_log(ffiles)

    svls._parse_ffiles(ffiles)

    # sourcePath = Path(unquote(urlparse(params.text_Document.uri).path)).resolve()
    # if len(svls.files) == 0 or params.text_document.uri.startswith('untitled:'):
    text_doc = ls.workspace.get_document(params.text_document.uri)
    # source = text_doc.source

    diagnostics = _validate_sv(text_doc) if (text_doc.source or (len(svls.files) > 0)) else []

    if len(diagnostics) > 0:
        for svf, diags in diagnostics.items():
            if str(svf).startswith('untitled:'):
                svf = text_doc.uri
            ls.publish_diagnostics(str(svf), diags)
    else:
        ls.publish_diagnostics(text_doc.uri, diagnostics)


def _validate_sv(text_doc):
    """Validates SV file."""
    diagnostics = {}

    comp = Compilation()
    sm = SourceManager()

    # Add uvm_pkg path to source manager
    if (svls.uvmPkgPath != ''):
        sm.addUserDirectory('%s/src' % svls.uvmPkgPath)

    # Resolve source path
    sourcePath = text_doc.uri
    if not sourcePath.startswith('untitled:'):
        sourcePath = Path(unquote(urlparse(text_doc.uri).path)).resolve()

    # Add file currently being edited
    if text_doc.source and not str(sourcePath).endswith('.f'):

        # scan for include directories currently missing (possible temporary based on slang improvements)
        includePaths = set()
        for line in text_doc.lines:
            m = includeFile.match(line)
            if m:
                includePaths.add(Path(m.group(1)).parent.resolve())

        for p in includePaths:
            sm.addUserDirectory(p)

        # Create buffer for source from client
        byteSource = bytes(text_doc.source, 'utf-8')
        sv = cppyy.gbl.string_view(byteSource)
        sv._buffer = byteSource
        buf = sm.assignText(
            str(sourcePath),
            sv
        )
        
        # Add buffer to comp unit
        t = SyntaxTree.fromBuffer(buf, sm)
        svls.files[sourcePath] = t
        comp.addSyntaxTree(t)

    # Add all files in the .f list, skipping the current one if it is in the list
    # If the current file is a `include file, adding it previously will be sufficient
    for svf, t in svls.files.items():
        if svf != sourcePath:
            p = str(svf)
            t = SyntaxTree.fromFile(p, sm)
            svls.files[svf] = t
            comp.addSyntaxTree(t)

    # Generate diagnostics for comp unit
    de = DiagnosticEngine(sm)
    client = JSONDiagnosticClient()
    de.addClient(client)

    for d in comp.getAllDiagnostics():
        de.issue(d)

    # Process diagnostic results
    results = client.getBuf()
    for res in results:

        # Resolve path
        path = Path(res['fileName'])
        if not res['fileName'].startswith('untitled:'):
            path = path.resolve()

        # Skip UVM package warnings if enabled
        if svls.ignoreUvmPackage:
            if str(Path(svls.uvmPkgPath).resolve()) in str(path) and res['severity'] >= 2:
                continue

        d = Diagnostic(
            range=Range(
                start=Position(line=res['lineNumber'], character=res['startCol']),
                end=Position(line=res['lineNumber'], character=res['endCol'])
            ),
            severity=DiagnosticSeverity(res['severity']),
            # code=res['code'],
            message=res['message'],
            source=type(svls).__name__
        )

        if path not in diagnostics:
            diagnostics[path] = []
        diagnostics[path].append(d)

    # print('\n\n')

    return diagnostics


@svls.feature(COMPLETION, CompletionOptions(trigger_characters=[',']))
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""
    return CompletionList(
        is_incomplete=False,
        items=[
            # CompletionItem(label='"'),
            # CompletionItem(label='['),
            # CompletionItem(label=']'),
            # CompletionItem(label='{'),
            # CompletionItem(label='}'),
        ]
    )

@svls.thread()
@svls.command(SVLanguageServer.CMD_COUNT_DOWN_BLOCKING)
def count_down_10_seconds_blocking(ls, *args):
    """Starts counting down and showing message synchronously.
    It will `block` the main thread, which can be tested by trying to show
    completion items.
    """
    for i in range(COUNT_DOWN_START_IN_SECONDS):
        ls.show_message(f'Counting down... {COUNT_DOWN_START_IN_SECONDS - i}')
        time.sleep(COUNT_DOWN_SLEEP_IN_SECONDS)


@svls.command(SVLanguageServer.CMD_COUNT_DOWN_NON_BLOCKING)
async def count_down_10_seconds_non_blocking(ls, *args):
    """Starts counting down and showing message asynchronously.
    It won't `block` the main thread, which can be tested by trying to show
    completion items.
    """
    for i in range(COUNT_DOWN_START_IN_SECONDS):
        ls.show_message(f'Counting down... {COUNT_DOWN_START_IN_SECONDS - i}')
        await asyncio.sleep(COUNT_DOWN_SLEEP_IN_SECONDS)


@svls.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    await _validate(ls, params)


@svls.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: SVLanguageServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message('Text Document Did Close')


@svls.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    ls.show_message('Text Document Did Open')
    await _validate(ls, params)


# @svls.feature(
#     TEXT_DOCUMENT_SEMANTIC_TOKENS,
#     SemanticTokensOptions(
#         legend=SemanticTokensLegend(
#             tokenTypes=[],
#             tokenModifiers=[]
#         )
#     )
# )
# async def semantic_tokens(ls):
#     """Used to signal to the client that we support tokens."""


@svls.feature(TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL)
def semantic_tokens_full(ls, params: SemanticTokensParams):
    """A 'full' semantic tokens request."""

    return SemanticTokens(data=[
        # deltaLine, deltaStart, length, tokenType, tokenModifiers
    ])


@svls.command(SVLanguageServer.CMD_PROGRESS)
async def progress(ls: SVLanguageServer, *args):
    """Create and start the progress on the client."""
    token = 'token'
    # Create
    await ls.progress.create_async(token)
    # Begin
    ls.progress.begin(token, WorkDoneProgressBegin(title='Indexing', percentage=0))
    # Report
    for i in range(1, 10):
        ls.progress.report(
            token,
            WorkDoneProgressReport(message=f'{i * 10}%', percentage= i * 10),
        )
        await asyncio.sleep(2)
    # End
    ls.progress.end(token, WorkDoneProgressEnd(message='Finished'))


@svls.command(SVLanguageServer.CMD_REGISTER_COMPLETIONS)
async def register_completions(ls: SVLanguageServer, *args):
    """Register completions method on the client."""
    params = RegistrationParams(registrations=[
                Registration(
                    id=str(uuid.uuid4()),
                    method=COMPLETION,
                    register_options={"triggerCharacters": "[':']"})
             ])
    response = await ls.register_capability_async(params)
    if response is None:
        ls.show_message('Successfully registered completions method')
    else:
        ls.show_message('Error happened during completions registration.',
                        MessageType.Error)


@svls.command(SVLanguageServer.CMD_SHOW_CONFIGURATION_ASYNC)
async def show_configuration_async(ls: SVLanguageServer, *args):
    """Gets slangFFileLists from the client settings using coroutines."""
    try:
        config = await ls.get_configuration_async(
            ConfigurationParams(items=[
                ConfigurationItem(
                    scope_uri='',
                    section=SVLanguageServer.CONFIGURATION_SECTION)
        ]))

        example_config = config[0].get('slangFFileLists')

        ls.show_message(f'SVLS.slangFFileLists value: {example_config}')

    except Exception as e:
        ls.show_message_log(f'Error ocurred: {e}')


@svls.command(SVLanguageServer.CMD_SHOW_CONFIGURATION_CALLBACK)
def show_configuration_callback(ls: SVLanguageServer, *args):
    """Gets slangFFileLists from the client settings using callback."""
    def _config_callback(config):
        try:
            example_config = config[0].get('slangFFileLists')

            ls.show_message(f'SVLS.slangFFileLists value: {example_config}')

        except Exception as e:
            ls.show_message_log(f'Error ocurred: {e}')

    ls.get_configuration(ConfigurationParams(items=[
        ConfigurationItem(
            scope_uri='',
            section=SVLanguageServer.CONFIGURATION_SECTION)
    ]), _config_callback)


@svls.thread()
@svls.command(SVLanguageServer.CMD_SHOW_CONFIGURATION_THREAD)
def show_configuration_thread(ls: SVLanguageServer, *args):
    """Gets slangFFileLists from the client settings using thread pool."""
    try:
        config = ls.get_configuration(ConfigurationParams(items=[
            ConfigurationItem(
                scope_uri='',
                section=SVLanguageServer.CONFIGURATION_SECTION)
        ])).result(2)

        example_config = config[0].get('slangFFileLists')

        ls.show_message(f'SVLS.slangFFileLists value: {example_config}')

    except Exception as e:
        ls.show_message_log(f'Error ocurred: {e}')


@svls.command(SVLanguageServer.CMD_UNREGISTER_COMPLETIONS)
async def unregister_completions(ls: SVLanguageServer, *args):
    """Unregister completions method on the client."""
    params = UnregistrationParams(unregisterations=[
        Unregistration(id=str(uuid.uuid4()), method=COMPLETION)
    ])
    response = await ls.unregister_capability_async(params)
    if response is None:
        ls.show_message('Successfully unregistered completions method')
    else:
        ls.show_message('Error happened during completions unregistration.',
                        MessageType.Error)
