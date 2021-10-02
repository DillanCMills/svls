from server.svcpp import *

import re
import os
from pathlib import Path

os.chdir('../../Documents/uvm_labs')

fcomment = re.compile(r'^\s*//')
svfile = re.compile(r'^\s*(.*\.s?vh?)\s*$')
ffile = re.compile(r'^\s*-[fF]\s+(.*\.f)\s*$')

def parse_ffile(file):
   files = {}
   if file.exists() and not file.is_dir():
      with file.open() as f:
         for line in f:
            if fcomment.match(line):
               continue
            svf = svfile.match(line)
            if svf:
               uvm = './uvm-1.2'
               svf = svf.group(1).replace('$UVM_HOME', uvm)
               filePath = (file.parent / Path(svf)).resolve()
               if filePath.exists() and not filePath.is_dir():
                  files[filePath] = None
   return files

ffile = Path('svls.f').resolve()

files = parse_ffile(ffile)

comp = Compilation()
sm = SourceManager()

sm.addUserDirectory('uvm-1.2/src')

for svf, t in files.items():
   if t is None:
      p = str(svf)
      t = SyntaxTree.fromFile(p, sm)
      files[svf] = t
   comp.addSyntaxTree(t)


text = cppyy.gbl.string_view('''
''')

buffer = sm.assignText(
   '',
   text
)

# print(text)
# print(buffer.data)

# t = SyntaxTree.fromBuffer(buffer, sm)
# comp.addSyntaxTree(t)

# de = DiagnosticEngine(sm)
# client = JSONDiagnosticClient()
# de.addClient(client)

# for d in comp.getAllDiagnostics():
#    de.issue(d)

# results = client.getBuf()
# for res in results:
#    print(res)


