import cppyy
# import cppyy.ll
from pathlib import Path

from .args import args

libP = Path(args.slangLib)
sourceP = Path(args.slangSource)

############################################################################
# Set up cppyy (runs from root directory)
############################################################################
# cppyy.ll.set_signals_as_exception(True)

cppyy.add_include_path(str(sourceP / 'include'))
cppyy.add_include_path(str(sourceP / 'external'))
cppyy.add_include_path(str(sourceP / 'build' / 'source'))

cppyy.include('slang/compilation/Compilation.h')
cppyy.include('slang/diagnostics/DiagnosticClient.h')
cppyy.include('slang/diagnostics/DiagnosticEngine.h')
cppyy.include('slang/syntax/SyntaxTree.h')
cppyy.include('slang/syntax/SyntaxNode.h')
cppyy.include('slang/syntax/SyntaxKind.h')
cppyy.include('slang/parsing/Token.h')
# cppyy.include('slang/syntax/SyntaxVisitor.h')
# cppyy.include('slang/symbols/ASTVisitor.h')
cppyy.include('slang/parsing/Lexer.h')
cppyy.include('slang/parsing/LexerFacts.h')

cppyy.include('slang/text/SourceManager.h')
cppyy.include('slang/text/SourceLocation.h')
cppyy.include('slang/util/SmallVector.h')

cppyy.load_library(str(libP / 'libslangcore'))
cppyy.load_library(str(libP / 'libslangparser'))
cppyy.load_library(str(libP / 'libslangruntime'))
cppyy.load_library(str(libP / 'libslangcompiler'))
############################################################################

slang = cppyy.gbl.slang
SyntaxTree = slang.SyntaxTree
Compilation = slang.Compilation
DiagnosticEngine = slang.DiagnosticEngine
SourceManager = slang.SourceManager
SyntaxNode = slang.SyntaxNode
Token = slang.Token
SyntaxKind = slang.SyntaxKind
syntaxKindLookup = dict([(value, key) for key, value in SyntaxKind.__dict__.items()])
TokenKind = slang.TokenKind
tokenKindLookup = dict([(value, key) for key, value in TokenKind.__dict__.items()])
SourceBuffer = slang.SourceBuffer
Diagnostics = slang.Diagnostics
Lexer = slang.Lexer
class JSONDiagnosticClient(slang.DiagnosticClient):

   def __init__(self):
      super().__init__()
      self.bufArr = []

   def trimRange(self, range: slang.SourceRange, caretLoc: slang.SourceLocation, col: int, sourceLine: str):
      start = range.start().offset()
      end = range.end().offset()
      startOfLine = caretLoc.offset() - col
      endOfLine = startOfLine + sourceLine.length()

      if (start < startOfLine):
         start = startOfLine
      if (end > endOfLine):
         end = endOfLine
      
      if (start >= end):
         return (col, col)

      start -= startOfLine
      end -= startOfLine
      # while (sourceLine[start] == ' ' or sourceLine[start] == '\t'):
      #    start += 1
      #    if (start == end):
      #       return (start, end)
      # while (sourceLine[end - 1] == ' ' or sourceLine[end - 1] == '\t'):
      #    end -= 1
      #    if (start == end):
      #       return (start, end)
      
      return (start, end)


   def convertSeverity(self, severity):
      if (severity >= 3):
         return 1
      elif (severity == 2):
         return 2
      else:
         return 3

   
   def report(self, diag: slang.ReportedDiagnostic):
      col = 0   
      buf = {}
      mappedRanges = slang.SmallVectorSized[slang.SourceRange, 8]()
      self.engine.mapSourceRanges(diag.location, diag.ranges, mappedRanges)

      if (diag.location != slang.SourceLocation.NoLocation):
         col = self.sourceManager.getColumnNumber(diag.location) - 1
         buf['fileName'] = str(self.sourceManager.getFileName(diag.location))
         buf['lineNumber'] = self.sourceManager.getLineNumber(diag.location) - 1
         buf['columnNumber'] = col
         buf['startCol'] = col
         buf ['endCol'] = col
         if len(mappedRanges) > 0:
            if len(mappedRanges) > 2:
               print('Warning: mappedRanges > 2')

            start, end = self.trimRange(mappedRanges[0], diag.location, col, self.getSourceLine(diag.location, col))
            # if (start != end):
            #    start = end
            buf['startCol'] = min(buf['startCol'], start)

            start, end = self.trimRange(mappedRanges[1], diag.location, col, self.getSourceLine(diag.location, col))
            # if (start != end):
            #    start = end
            buf['endCol'] = max(buf['endCol'], end)

      buf['severity'] = self.convertSeverity(diag.severity)
      # print(diag.originalDiagnostic.code, str(diag.originalDiagnostic.code))
      # buf['code'] = str(diag.code)
      buf['message'] = str(diag.formattedMessage)

      self.bufArr.append(buf)

   def getBuf(self):
      return self.bufArr


class Visitor():

   def visitToken(self, token: Token):
      # print('Visiting token:', token)
      trivia = [str(x.getRawText()) for x in token.trivia()]
      print('{%s: %s}' % (
         tokenKindLookup.get(token.kind, token.kind),
         str(token.valueText())))
      if len(trivia) > 0:
         print('    ', trivia)

   def walkTree(self, node: SyntaxNode):
      # print('Visiting node:', node)
      # print('node:', node.toString().replace(' ', '-').replace('\n', '\\n'))
      # print('')
      for i in range(node.getChildCount()):
         child = node.childNode(i)
         if (child):
            self.walkTree(child)
         else:
            token = node.childToken(i)
            if (token):
               self.visitToken(token)


# class NodeRewriter(Rewriter):
#    # pass   
#    def visit(self, node: SyntaxNode):
#       print('Visitng node:', node)
#       super().visit(node)

   # def handle(self, node: SyntaxNode):
   #    print('Handling node:', node)
   #    # super.handle(node)

# class Visitor(ASTVisitor[SyntaxNode, True, True]):
#    pass

# class Rewriter(NodeRewriter):

#    def __init__(self):
#       super().__init__()
#       self.count = 0

   # def visit(self, node: SyntaxNode):
   #    print('Visiting node:', node)
   # #    super().visit[SyntaxNode](node)

   # def visitDefault(self, node: SyntaxNode):
   #    print('Visitng default node:', node)

   # def handle(self, node: SyntaxNode):
   #    print('Handling node:', node)
   #    self.count += 1
   #    super().visitDefault(node)
      # self.visit[SyntaxNode](node)
