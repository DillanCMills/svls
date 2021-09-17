import cppyy
import cppyy.ll
from pathlib import Path

from .args import args

libP = Path(args.slangLib)
sourceP = Path(args.slangSource)

############################################################################
# Set up cppyy (runs from root directory)
############################################################################
cppyy.ll.set_signals_as_exception(True)

cppyy.add_include_path(str(sourceP / 'include'))
cppyy.add_include_path(str(sourceP / 'external'))
cppyy.add_include_path(str(sourceP / 'build' / 'source'))

cppyy.include('slang/compilation/Compilation.h')
cppyy.include('slang/diagnostics/DiagnosticClient.h')
cppyy.include('slang/diagnostics/DiagnosticEngine.h')
cppyy.include('slang/syntax/SyntaxTree.h')

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