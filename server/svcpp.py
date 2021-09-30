from os import stat
import cppyy
from cppyy import addressof, bind_object
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

cppyy.include('slang/binding/AssignmentExpressions.h')
cppyy.include('slang/binding/BindContext.h')
cppyy.include('slang/binding/Constraints.h')
cppyy.include('slang/binding/Expression.h')
cppyy.include('slang/binding/EvalContext.h')
cppyy.include('slang/binding/LiteralExpressions.h')
cppyy.include('slang/binding/MiscExpressions.h')
cppyy.include('slang/binding/OperatorExpressions.h')
cppyy.include('slang/binding/Statements.h')
cppyy.include('slang/binding/TimingControl.h')
cppyy.include('slang/compilation/Compilation.h')
cppyy.include('slang/compilation/Definition.h')
cppyy.include('slang/compilation/DesignTree.h')
cppyy.include('slang/diagnostics/DiagnosticClient.h')
cppyy.include('slang/diagnostics/DiagnosticEngine.h')
cppyy.include('slang/numeric/ConstantValue.h')
cppyy.include('slang/parsing/Lexer.h')
cppyy.include('slang/parsing/LexerFacts.h')
cppyy.include('slang/parsing/Token.h')
cppyy.include('slang/symbols/ASTSerializer.h')
# cppyy.include('slang/symbols/ASTVisitor.h')
cppyy.include('slang/symbols/BlockSymbols.h')
cppyy.include('slang/symbols/CompilationUnitSymbols.h')
cppyy.include('slang/symbols/InstanceSymbols.h')
cppyy.include('slang/symbols/ParameterSymbols.h')
cppyy.include('slang/symbols/PortSymbols.h')
cppyy.include('slang/symbols/Scope.h')
cppyy.include('slang/symbols/SemanticFacts.h')
cppyy.include('slang/symbols/Symbol.h')
cppyy.include('slang/symbols/ValueSymbol.h')
cppyy.include('slang/symbols/VariableSymbols.h')
cppyy.include('slang/syntax/SyntaxKind.h')
cppyy.include('slang/syntax/SyntaxNode.h')
cppyy.include('slang/syntax/SyntaxTree.h')
# cppyy.include('slang/syntax/SyntaxVisitor.h')
cppyy.include('slang/text/Json.h')
cppyy.include('slang/text/SourceLocation.h')
cppyy.include('slang/text/SourceManager.h')
cppyy.include('slang/types/AllTypes.h')
cppyy.include('slang/types/Type.h')
cppyy.include('slang/util/BumpAllocator.h')
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
SymbolKind = slang.SymbolKind
symbolKindLookup = dict([(value, key) for key, value in SymbolKind.__dict__.items()])
SourceBuffer = slang.SourceBuffer
Diagnostics = slang.Diagnostics
Lexer = slang.Lexer
BumpAllocator = slang.BumpAllocator
DesignTreeNode = slang.DesignTreeNode
Symbol = slang.Symbol
Scope = slang.Scope
next = cppyy.gbl.std.next
JsonWriter = slang.JsonWriter
ASTSerializer = slang.ASTSerializer
Expression = slang.Expression
EvalContext = slang.EvalContext
EvalFlags = slang.EvalFlags
ConstantValue = slang.ConstantValue
Statement = slang.Statement
Type = slang.Type
TypeAliasType = slang.TypeAliasType
TimingControl = slang.TimingControl
TimingControlKind = slang.TimingControlKind
timingControlKindLookup = dict([(value, key) for key, value in TimingControlKind.__dict__.items()])
Constraint = slang.Constraint
AssertionExpr = slang.AssertionExpr
ValueSymbol = slang.ValueSymbol
InstanceSymbol = slang.InstanceSymbol
VariableSymbol = slang.VariableSymbol
VariableLifetime = slang.VariableLifetime
variableLifetimeLookup = dict([(value, key) for key, value in VariableLifetime.__dict__.items()])
ProceduralBlockSymbol = slang.ProceduralBlockSymbol
ProceduralBlockKind = slang.ProceduralBlockKind
proceduralBlockKindLookup = dict([(value, key) for key, value in ProceduralBlockKind.__dict__.items()])
StatementKind = slang.StatementKind
statementKindLookup = dict({(value, key) for key, value in StatementKind.__dict__.items()})
ParameterSymbol = slang.ParameterSymbol
PortSymbol = slang.PortSymbol
ArgumentDirection = slang.ArgumentDirection
argumentDirectionLookup = dict([(value, key) for key, value in ArgumentDirection.__dict__.items()])
EdgeKind = slang.EdgeKind
edgeKindLookup = dict({(value, key) for key, value in EdgeKind.__dict__.items()})
ExpressionKind = slang.ExpressionKind
expressionKindLookup = dict([(value, key) for key, value in ExpressionKind.__dict__.items()])
StatementBlockKind = slang.StatementBlockKind
statementBlockKindLookup = dict([(value, key) for key, value in StatementBlockKind.__dict__.items()])
BinaryOperator = slang.BinaryOperator
binaryOperatorLookup = dict([(value, key) for key, value in BinaryOperator.__dict__.items()])

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

   def __init__(self, comp: Compilation, sm: SourceManager):
      self.tokens = []
      self.internalSymbols = []
      self.comp = comp
      self.sm = sm


   def visitToken(self, token: Token, count):
      # print('Visiting token:', token)
      trivia = [str(x.getRawText()) for x in token.trivia()]
      print('%s| {%s: %s}' % (
         '-'*count,
         tokenKindLookup.get(token.kind, token.kind),
         str(token.valueText())))
      if len(trivia) > 0:
         print('    ', trivia)


   def walkSyntaxTree(self, node: SyntaxNode, count=1):
      # print('Visiting node:', node)
      # print('node:', node.toString().replace(' ', '-').replace('\n', '\\n'))
      # print('')
      print('%s> {%s: %s}' % (
         '-'*count,
         syntaxKindLookup.get(node.kind, node.kind),
         str(node.toString())
      ))
      for i in range(node.getChildCount()):
         child = node.childNode(i)
         if (child):
            self.walkSyntaxTree(child, count+1)
         else:
            token = node.childToken(i)
            if (token):
               self.visitToken(token, count)


   def walkDesignTree(self, elem: Symbol):
      if isinstance(elem, slang.RootSymbol):
         if elem.kind == 1:  # Root
            for m in elem.members():
               self.walkDesignTree(m)

      elif isinstance(elem, slang.Symbol):
         if elem.kind == 2:  # CompilationUnit
            return

         elif elem.kind == 42:  # Instance
            inst = bind_object(addressof(elem), slang.InstanceSymbol)
            
            # body
            self.walkDesignTree(inst.body)

         elif elem.kind == 43:  # InstanceBody
            newToken = {
               'name': str(elem.name),
               'kind': symbolKindLookup[elem.kind],
               'addr': addressof(elem),
               'definition': str(elem.getDefinition().name),
               'fileName': str(self.sm.getFileName(elem.location)),
               'lineNumber': self.sm.getLineNumber(elem.location),
               'columnNumber': self.sm.getColumnNumber(elem.location)
            }

            self.tokens.append(newToken)

            # members
            for m in elem.members():
               self.walkDesignTree(m)

         elif elem.kind == 36:  # Parameter
            param = bind_object(elem, slang.ParameterSymbol)
            newToken = {
               'name': str(param.name),
               'kind': symbolKindLookup[param.kind],
               'addr': addressof(param),
               'type': str(param.getType().toString()),
               'value': str(param.getValue().toString()),
               'isLocal': param.isLocalParam(),
               'isPort': param.isPortParam(),
               'isBody': param.isBodyParam(),
               'fileName': str(self.sm.getFileName(param.location)),
               'lineNumber': self.sm.getLineNumber(param.location),
               'columnNumber': self.sm.getColumnNumber(param.location)
            }

            self.tokens.append(newToken)

         elif elem.kind == 38:  # Port
            port = bind_object(elem, slang.PortSymbol)
            newToken = {
               'name': str(port.name),
               'kind': symbolKindLookup[port.kind],
               'addr': addressof(port),
               'type': str(port.getType().toString()),
               'direction': argumentDirectionLookup[port.direction],
               'internalSymbolAddr': addressof(port.internalSymbol), 
               'internalSymbolName': str(port.internalSymbol.name),
               'fileName': str(self.sm.getFileName(port.location)),
               'lineNumber': self.sm.getLineNumber(port.location),
               'columnNumber': self.sm.getColumnNumber(port.location)
            }
            self.internalSymbols.append(addressof(port.internalSymbol))

            self.tokens.append(newToken)

         elif elem.kind == 55:  # Variable
            var = bind_object(elem, slang.VariableSymbol)

            if addressof(var) in self.internalSymbols:
               return

            newToken = {
               'name': str(var.name),
               'kind': symbolKindLookup[var.kind],
               'addr': addressof(var),
               'type': str(var.getType().toString()),
               'lifetime': variableLifetimeLookup[var.lifetime],
               'isConstant': var.isConstant,
               'isCompilerGenerated': var.isCompilerGenerated,
               'fileName': str(self.sm.getFileName(var.location)),
               'lineNumber': self.sm.getLineNumber(var.location),
               'columnNumber': self.sm.getColumnNumber(var.location)
            }

            self.tokens.append(newToken)

         elif elem.kind == 52:  # ProceduralBlock
            block = bind_object(elem, slang.ProceduralBlockSymbol)
            newToken = {
               'name': str(block.name),
               'kind': symbolKindLookup[block.kind],
               'addr': addressof(block),
               'procedureKind': proceduralBlockKindLookup[block.procedureKind],
               'fileName': str(self.sm.getFileName(block.location)),
               'lineNumber': self.sm.getLineNumber(block.location),
               'columnNumber': self.sm.getColumnNumber(block.location)
            }

            # self.tokens.append(newToken)

            # body
            self.walkDesignTree(block.getBody())

      elif isinstance(elem, Statement):
         if elem.kind == 18:  # Timed
            stmt = bind_object(elem, slang.TimedStatement)
            # newToken = {
            #    'kind': statementKindLookup[stmt.kind]
            # }

            self.walkDesignTree(stmt.timing)
            self.walkDesignTree(stmt.stmt)

         elif elem.kind == 3:  # Block
            block = bind_object(elem, slang.BlockStatement)
            newToken = {
               'kind': statementKindLookup[block.kind],
               'blockKind': statementBlockKindLookup[block.blockKind],
               'fileNameStart': str(self.sm.getFileName(block.sourceRange.start())),
               'lineNumberStart': self.sm.getLineNumber(block.sourceRange.start()),
               'columnNumberStart': self.sm.getColumnNumber(block.sourceRange.start()),
               'fileNameEnd': str(self.sm.getFileName(block.sourceRange.end())),
               'lineNumberEnd': self.sm.getLineNumber(block.sourceRange.end()),
               'columnNumberEnd': self.sm.getColumnNumber(block.sourceRange.end())
            }

            # self.tokens.append(newToken)

            self.walkDesignTree(block.getStatements())

         elif elem.kind == 2:  # List
            lst = bind_object(elem, slang.StatementList)

            for l in lst.list:
               self.walkDesignTree(l)

         elif elem.kind == 4:  # Expression Statement
            expr = bind_object(elem, slang.ExpressionStatement)
            # newToken = {
            #    'kind': statementKindLookup[expr.kind],
            #    'fileNameStart': str(self.sm.getFileName(expr.expr.sourceRange.start())),
            #    'lineNumberStart': self.sm.getLineNumber(expr.expr.sourceRange.start()),
            #    'columnNumberStart': self.sm.getColumnNumber(expr.expr.sourceRange.start()),
            #    'fileNameEnd': str(self.sm.getFileName(expr.expr.sourceRange.end())),
            #    'lineNumbeEndr': self.sm.getLineNumber(expr.expr.sourceRange.end()),
            #    'columnNumberEnd': self.sm.getColumnNumber(expr.expr.sourceRange.end())
            # }

            if expr.expr.kind == 14:  # Assignment
               assign = bind_object(expr.expr, slang.AssignmentExpression)
               # newToken['exprKind'] = expressionKindLookup[expr.expr.kind]
               # newToken['exprLeftKind'],
               # newToken['exprLeftType'],
               # newToken['exprLeftSymbolAddr'],
               # newToken['exprLeftSymbolName'],
               # newToken['exprRightKind'],
               # newToken['exprRightType'],
               # newToken['exprRightOp'],
               # newToken['exprRightSymbolAddr'],
               # newToken['exprRightSymbolName'],
               self.walkDesignTree(assign.left())

               newToken = {
                  'kind': expressionKindLookup[assign.kind],
                  'type': str(assign.type.toString()),
                  'isNonBlocking': assign.isNonBlocking(),
                  'fileNameStart': str(self.sm.getFileName(assign.sourceRange.start())),
                  'lineNumberStart': self.sm.getLineNumber(assign.sourceRange.start()),
                  'columnNumberStart': self.sm.getColumnNumber(assign.sourceRange.start()),
                  'fileNameEnd': str(self.sm.getFileName(assign.sourceRange.end())),
                  'lineNumbeEndr': self.sm.getLineNumber(assign.sourceRange.end()),
                  'columnNumberEnd': self.sm.getColumnNumber(assign.sourceRange.end())
               }
               if assign.op.has_value():
                  newToken['op'] = binaryOperatorLookup[assign.op.value()]

               # self.tokens.append(newToken)

               self.walkDesignTree(assign.right())


      elif isinstance(elem, slang.Expression):
         if elem.kind == 8:  # NamedValue
            expr = bind_object(elem, slang.NamedValueExpression)
            newToken = {
               'kind': expressionKindLookup[expr.kind],
               'type': str(expr.type.toString()),
               'symbolAddr': addressof(expr.getSymbolReference()),
               'symbolName': str(expr.getSymbolReference().name),
               'fileNameStart': str(self.sm.getFileName(expr.sourceRange.start())),
               'lineNumberStart': self.sm.getLineNumber(expr.sourceRange.start()),
               'columnNumberStart': self.sm.getColumnNumber(expr.sourceRange.start()),
               'fileNameEnd': str(self.sm.getFileName(expr.sourceRange.end())),
               'lineNumbeEndr': self.sm.getLineNumber(expr.sourceRange.end()),
               'columnNumberEnd': self.sm.getColumnNumber(expr.sourceRange.end())
            }

            self.tokens.append(newToken)

         elif elem.kind == 11:  # BinaryOp
            expr = bind_object(elem, slang.BinaryExpression)

            self.walkDesignTree(expr.left())

            newToken = {
               'kind': expressionKindLookup[expr.kind],
               'type': str(expr.type.toString()),
               'op': binaryOperatorLookup[expr.op],
               'fileNameStart': str(self.sm.getFileName(expr.sourceRange.start())),
               'lineNumberStart': self.sm.getLineNumber(expr.sourceRange.start()),
               'columnNumberStart': self.sm.getColumnNumber(expr.sourceRange.start()),
               'fileNameEnd': str(self.sm.getFileName(expr.sourceRange.end())),
               'lineNumbeEndr': self.sm.getLineNumber(expr.sourceRange.end()),
               'columnNumberEnd': self.sm.getColumnNumber(expr.sourceRange.end())
            }

            # self.tokens.append(newToken)

            self.walkDesignTree(expr.right())

         elif elem.kind == 26:  # LValueReference
            expr = bind_object(elem, slang.LValueReferenceExpression)
            newToken = {
               'kind': expressionKindLookup[expr.kind],
               'type': str(expr.type.toString()),
               'fileNameStart': str(self.sm.getFileName(expr.sourceRange.start())),
               'lineNumberStart': self.sm.getLineNumber(expr.sourceRange.start()),
               'columnNumberStart': self.sm.getColumnNumber(expr.sourceRange.start()),
               'fileNameEnd': str(self.sm.getFileName(expr.sourceRange.end())),
               'lineNumbeEndr': self.sm.getLineNumber(expr.sourceRange.end()),
               'columnNumberEnd': self.sm.getColumnNumber(expr.sourceRange.end())
            }

            # self.tokens.append(newToken)

         elif elem.kind == 22:  # Conversion
            expr = bind_object(elem, slang.ConversionExpression)
            newToken = {
               'kind': expressionKindLookup[expr.kind],
               'type': str(expr.type.toString()),
               'constant': str(expr.constant.toString()),
               'fileNameStart': str(self.sm.getFileName(expr.sourceRange.start())),
               'lineNumberStart': self.sm.getLineNumber(expr.sourceRange.start()),
               'columnNumberStart': self.sm.getColumnNumber(expr.sourceRange.start()),
               'fileNameEnd': str(self.sm.getFileName(expr.sourceRange.end())),
               'lineNumbeEndr': self.sm.getLineNumber(expr.sourceRange.end()),
               'columnNumberEnd': self.sm.getColumnNumber(expr.sourceRange.end())
            }

            if expr.operand().kind == 1:  # IntegerLiteral
               operand = bind_object(expr.operand(), slang.IntegerLiteral)
               newToken['operandKind'] = expressionKindLookup[operand.kind]
               newToken['operandType'] = str(operand.type.toString())
               newToken['operandValue'] = str(operand.getValue().toString())
               newToken['operandConstant'] = str(operand.constant.toString())

            self.tokens.append(newToken)
               


      elif isinstance(elem, slang.TimingControl):

         if elem.kind == 2:  # Signal Event
            timing = bind_object(elem, slang.SignalEventControl)

            newToken = {
               'kind': timingControlKindLookup[timing.kind],
               'edge': edgeKindLookup[timing.edge],
               'fileNameStart': str(self.sm.getFileName(timing.expr.sourceRange.start())),
               'lineNumberStart': self.sm.getLineNumber(timing.expr.sourceRange.start()),
               'columnNumberStart': self.sm.getColumnNumber(timing.expr.sourceRange.start()),
               'fileNameEnd': str(self.sm.getFileName(timing.expr.sourceRange.end())),
               'lineNumbeEndr': self.sm.getLineNumber(timing.expr.sourceRange.end()),
               'columnNumberEnd': self.sm.getColumnNumber(timing.expr.sourceRange.end())
            }

            expr = timing.expr
            if expr.kind == 8:  # NamedValue
               newToken['exprKind'] = expressionKindLookup[expr.kind]
               newToken['exprType'] = str(expr.type.toString())
               newToken['exprSymbolAddr'] = addressof(expr.getSymbolReference())
               newToken['exprSymbolName'] = str(expr.getSymbolReference().name)

            self.tokens.append(newToken)


         elif elem.kind == 3:  # Event List
            timingList = bind_object(elem, slang.EventListControl)
            for timing in timingList.events:
               self.walkDesignTree(timing)
                  





      # if isinstance(elem, Expression):
      #    newToken = {'kind': symbolKindLookup[elem.kind], 'type': elem.type}
         
      #    if (type(elem) != Expression):
      #       print('TODO (e):', type(elem))

      #    ctx = EvalContext(self.comp, EvalFlags.CacheResults)
      #    constant: ConstantValue = elem.eval(ctx)
      #    if (constant):
      #       newToken['constant'] = constant

      #    self.tokens.append(newToken)

      # elif isinstance(elem, Statement):
      #    newToken = {'kind': symbolKindLookup[elem.kind]}

      #    if (type(elem) != Statement):
      #       print('TODO (s):', type(elem))

      #    self.tokens.append(newToken)

      # elif isinstance(elem, Type) and (type(elem) != TypeAliasType):
      #    return elem.toString()

      # elif isinstance(elem, TimingControl) or isinstance(elem, Constraint) or isinstance(elem, AssertionExpr):
      #    newToken = {'kind': symbolKindLookup[elem.kind]}

      #    if (type(elem) != TimingControl) and (type(elem) != Constraint) and (type(elem) != AssertionExpr):
      #       print('TODO (a):', type(elem))
         
      #    self.tokens.append(newToken)

      # else:
      #    newToken = {
      #       'name': elem.name, 
      #       'kind': symbolKindLookup[elem.kind],
      #       'addr': hex(int(elem.__repr__().partition('object at ')[2].strip('>'), 16))
      #    }

      #    scope = elem.getParentScope()
      #    if scope:
      #       attributes = scope.getCompilation().getAttributes(elem)
      #       if not attributes.empty():
      #          newToken['attributes'] = [a.toString() for a in attributes]

      #    if isinstance(elem, ValueSymbol):
      #       newToken['type'] = elem.getType()

      #       if init := elem.getInitializer():
      #          newToken['initializer'] = init

      #    if isinstance(elem, Scope):
      #       if not elem.empty():
      #          newToken['members'] = [a.toString() for a in elem.members()]

      #    if not type(elem) == Symbol:
      #       print('TODO: (sy):', type(elem))

      #    self.tokens.append(newToken)


      # for i in range(symbol.members().size()):
      #    next(symbol.members().begin(), i)



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


SemanticTokenTypes = {
	0 : 'namespace',      # namespace
	# Represents a generic type. Acts as a fallback for types which
	# can't be mapped to a specific type like class or enum.
	1  : 'type',          # type
	2  : 'class',         # class
	3  : 'enum',          # enum
	4  : 'interface',     # interface
	5  : 'struct',        # struct
	6  : 'typeParameter', # typeParameter
	7  : 'parameter',     # parameter
	8  : 'variable',      # variable
	9  : 'property',      # property
	10 : 'enumMember',    # enumMember
	11 : 'event',         # event
	12 : 'function',      # function
	13 : 'method',        # method
	14 : 'macro',         # macro
	15 : 'keyword',       # keyword
	16 : 'modifier',      # modifier
	17 : 'comment',       # comment
	18 : 'string',        # string
	19 : 'number',        # number
	20 : 'regexp',        # regexp
	21 : 'operator',      # operator
}

SemanticTokenModifiers = {
	0 : 'declaration',    # declaration
	1 : 'definition',     # definition
	2 : 'readonly',       # readonly
	3 : 'static',         # static
	4 : 'deprecated',     # deprecated
	5 : 'abstract',       # abstract
	6 : 'async',          # async
	7 : 'modification',   # modification
	8 : 'documentation',  # documentation
	9 : 'defaultLibrary', # defaultLibrary
}


tokenTypeMap = {
   # general
   # 0: 1,     #  Unknown
   # 1: 1,     #  EndOfFile
   # 2: 1,     #  Identifier
   3: 12,    #  SystemIdentifier
   4: 18,    #  StringLiteral
   5: 19,    #  IntegerLiteral
   6: 19,    #  IntegerBase
   7: 19,    #  UnbasedUnsizedLiteral
   8: 19,    #  RealLiteral
   9: 19,    #  TimeLiteral
   # 10: 1,    #  Placeholder

   # punctuation
   # 11: 11,   #  Apostrophe
   # 12: 12,   #  ApostropheOpenBrace
   # 13: 13,   #  OpenBrace
   # 14: 14,   #  CloseBrace
   # 15: 15,   #  OpenBracket
   # 16: 16,   #  CloseBracket
   # 17: 17,   #  OpenParenthesis
   # 18: 18,   #  OpenParenthesisStar
   # 19: 19,   #  CloseParenthesis
   # 20: 20,   #  StarCloseParenthesis
   # 21: 21,   #  Semicolon
   22: 21,   #  Colon
   23: 21,   #  ColonEquals
   24: 21,   #  ColonSlash
   25: 21,   #  DoubleColon
   # 26: 26,   #  Comma
   # 27: 27,   #  DotStar
   # 28: 28,   #  Dot
   29: 21,   #  Slash
   30: 21,   #  Star
   31: 21,   #  DoubleStar
   32: 21,   #  StarArrow
   33: 21,   #  Plus
   34: 21,   #  DoublePlus
   35: 21,   #  PlusColon
   36: 21,   #  Minus
   37: 21,   #  DoubleMinus
   38: 21,   #  MinusColon
   39: 21,   #  MinusArrow
   40: 21,   #  MinusDoubleArrow
   41: 21,   #  Tilde
   42: 21,   #  TildeAnd
   43: 21,   #  TildeOr
   44: 21,   #  TildeXor
   45: 21,   #  Dollar
   46: 21,   #  Question
   47: 21,   #  Hash
   48: 21,   #  DoubleHash
   49: 21,   #  HashMinusHash
   50: 21,   #  HashEqualsHash
   51: 21,   #  Xor
   52: 21,   #  XorTilde
   53: 21,   #  Equals
   54: 21,   #  DoubleEquals
   55: 21,   #  DoubleEqualsQuestion
   56: 21,   #  TripleEquals
   57: 21,   #  EqualsArrow
   58: 21,   #  PlusEqual
   59: 21,   #  MinusEqual
   60: 21,   #  SlashEqual
   61: 21,   #  StarEqual
   62: 21,   #  AndEqual
   63: 21,   #  OrEqual
   64: 21,   #  PercentEqual
   65: 21,   #  XorEqual
   66: 21,   #  LeftShiftEqual
   67: 21,   #  TripleLeftShiftEqual
   68: 21,   #  RightShiftEqual
   69: 21,   #  TripleRightShiftEqual
   70: 21,   #  LeftShift
   71: 21,   #  RightShift
   72: 21,   #  TripleLeftShift
   73: 21,   #  TripleRightShift
   74: 21,   #  Exclamation
   75: 21,   #  ExclamationEquals
   76: 21,   #  ExclamationEqualsQuestion
   77: 21,   #  ExclamationDoubleEquals
   78: 21,   #  Percent
   79: 21,   #  LessThan
   80: 21,   #  LessThanEquals
   81: 21,   #  LessThanMinusArrow
   82: 21,   #  GreaterThan
   83: 21,   #  GreaterThanEquals
   84: 21,   #  Or
   85: 21,   #  DoubleOr
   86: 21,   #  OrMinusArrow
   87: 21,   #  OrEqualsArrow
   88: 21,   #  At
   89: 21,   #  DoubleAt
   90: 21,   #  And
   91: 21,   #  DoubleAnd
   92: 21,   #  TripleAnd

   # keywords
   93: 15,   #  OneStep
   94: 15,   #  AcceptOnKeyword
   95: 15,   #  AliasKeyword
   96: 15,   #  AlwaysKeyword
   97: 15,   #  AlwaysCombKeyword
   98: 15,   #  AlwaysFFKeyword
   99: 15,   #  AlwaysLatchKeyword
   100: 15,  #  AndKeyword
   101: 15,  #  AssertKeyword
   102: 15,  #  AssignKeyword
   103: 15,  #  AssumeKeyword
   104: 15,  #  AutomaticKeyword
   105: 15,  #  BeforeKeyword
   106: 15,  #  BeginKeyword
   107: 15,  #  BindKeyword
   108: 15,  #  BinsKeyword
   109: 15,  #  BinsOfKeyword
   110: 15,  #  BitKeyword
   111: 15,  #  BreakKeyword
   112: 15,  #  BufKeyword
   113: 15,  #  BufIf0Keyword
   114: 15,  #  BufIf1Keyword
   115: 15,  #  ByteKeyword
   116: 15,  #  CaseKeyword
   117: 15,  #  CaseXKeyword
   118: 15,  #  CaseZKeyword
   119: 15,  #  CellKeyword
   120: 15,  #  CHandleKeyword
   121: 15,  #  CheckerKeyword
   122: 15,  #  ClassKeyword
   123: 15,  #  ClockingKeyword
   124: 15,  #  CmosKeyword
   125: 15,  #  ConfigKeyword
   126: 15,  #  ConstKeyword
   127: 15,  #  ConstraintKeyword
   128: 15,  #  ContextKeyword
   129: 15,  #  ContinueKeyword
   130: 15,  #  CoverKeyword
   131: 15,  #  CoverGroupKeyword
   132: 15,  #  CoverPointKeyword
   133: 15,  #  CrossKeyword
   134: 15,  #  DeassignKeyword
   135: 15,  #  DefaultKeyword
   136: 15,  #  DefParamKeyword
   137: 15,  #  DesignKeyword
   138: 15,  #  DisableKeyword
   139: 15,  #  DistKeyword
   140: 15,  #  DoKeyword
   141: 15,  #  EdgeKeyword
   142: 15,  #  ElseKeyword
   143: 15,  #  EndKeyword
   144: 15,  #  EndCaseKeyword
   145: 15,  #  EndCheckerKeyword
   146: 15,  #  EndClassKeyword
   147: 15,  #  EndClockingKeyword
   148: 15,  #  EndConfigKeyword
   149: 15,  #  EndFunctionKeyword
   150: 15,  #  EndGenerateKeyword
   151: 15,  #  EndGroupKeyword
   152: 15,  #  EndInterfaceKeyword
   153: 15,  #  EndModuleKeyword
   154: 15,  #  EndPackageKeyword
   155: 15,  #  EndPrimitiveKeyword
   156: 15,  #  EndProgramKeyword
   157: 15,  #  EndPropertyKeyword
   158: 15,  #  EndSpecifyKeyword
   159: 15,  #  EndSequenceKeyword
   160: 15,  #  EndTableKeyword
   161: 15,  #  EndTaskKeyword
   162: 15,  #  EnumKeyword
   163: 15,  #  EventKeyword
   164: 15,  #  EventuallyKeyword
   165: 15,  #  ExpectKeyword
   166: 15,  #  ExportKeyword
   167: 15,  #  ExtendsKeyword
   168: 15,  #  ExternKeyword
   169: 15,  #  FinalKeyword
   170: 15,  #  FirstMatchKeyword
   171: 15,  #  ForKeyword
   172: 15,  #  ForceKeyword
   173: 15,  #  ForeachKeyword
   174: 15,  #  ForeverKeyword
   175: 15,  #  ForkKeyword
   176: 15,  #  ForkJoinKeyword
   177: 15,  #  FunctionKeyword
   178: 15,  #  GenerateKeyword
   179: 15,  #  GenVarKeyword
   180: 15,  #  GlobalKeyword
   181: 15,  #  HighZ0Keyword
   182: 15,  #  HighZ1Keyword
   183: 15,  #  IfKeyword
   184: 15,  #  IffKeyword
   185: 15,  #  IfNoneKeyword
   186: 15,  #  IgnoreBinsKeyword
   187: 15,  #  IllegalBinsKeyword
   188: 15,  #  ImplementsKeyword
   189: 15,  #  ImpliesKeyword
   190: 15,  #  ImportKeyword
   191: 15,  #  IncDirKeyword
   192: 15,  #  IncludeKeyword
   193: 15,  #  InitialKeyword
   194: 15,  #  InOutKeyword
   195: 15,  #  InputKeyword
   196: 15,  #  InsideKeyword
   197: 15,  #  InstanceKeyword
   198: 15,  #  IntKeyword
   199: 15,  #  IntegerKeyword
   200: 15,  #  InterconnectKeyword
   201: 15,  #  InterfaceKeyword
   202: 15,  #  IntersectKeyword
   203: 15,  #  JoinKeyword
   204: 15,  #  JoinAnyKeyword
   205: 15,  #  JoinNoneKeyword
   206: 15,  #  LargeKeyword
   207: 15,  #  LetKeyword
   208: 15,  #  LibListKeyword
   209: 15,  #  LibraryKeyword
   210: 15,  #  LocalKeyword
   211: 15,  #  LocalParamKeyword
   212: 15,  #  LogicKeyword
   213: 15,  #  LongIntKeyword
   214: 15,  #  MacromoduleKeyword
   215: 15,  #  MatchesKeyword
   216: 15,  #  MediumKeyword
   217: 15,  #  ModPortKeyword
   218: 15,  #  ModuleKeyword
   219: 15,  #  NandKeyword
   220: 15,  #  NegEdgeKeyword
   221: 15,  #  NetTypeKeyword
   222: 15,  #  NewKeyword
   223: 15,  #  NextTimeKeyword
   224: 15,  #  NmosKeyword
   225: 15,  #  NorKeyword
   226: 15,  #  NoShowCancelledKeyword
   227: 15,  #  NotKeyword
   228: 15,  #  NotIf0Keyword
   229: 15,  #  NotIf1Keyword
   230: 15,  #  NullKeyword
   231: 15,  #  OrKeyword
   232: 15,  #  OutputKeyword
   233: 15,  #  PackageKeyword
   234: 15,  #  PackedKeyword
   235: 15,  #  ParameterKeyword
   236: 15,  #  PmosKeyword
   237: 15,  #  PosEdgeKeyword
   238: 15,  #  PrimitiveKeyword
   239: 15,  #  PriorityKeyword
   240: 15,  #  ProgramKeyword
   241: 15,  #  PropertyKeyword
   242: 15,  #  ProtectedKeyword
   243: 15,  #  Pull0Keyword
   244: 15,  #  Pull1Keyword
   245: 15,  #  PullDownKeyword
   246: 15,  #  PullUpKeyword
   247: 15,  #  PulseStyleOnDetectKeyword
   248: 15,  #  PulseStyleOnEventKeyword
   249: 15,  #  PureKeyword
   250: 15,  #  RandKeyword
   251: 15,  #  RandCKeyword
   252: 15,  #  RandCaseKeyword
   253: 15,  #  RandSequenceKeyword
   254: 15,  #  RcmosKeyword
   255: 15,  #  RealKeyword
   256: 15,  #  RealTimeKeyword
   257: 15,  #  RefKeyword
   258: 15,  #  RegKeyword
   259: 15,  #  RejectOnKeyword
   260: 15,  #  ReleaseKeyword
   261: 15,  #  RepeatKeyword
   262: 15,  #  RestrictKeyword
   263: 15,  #  ReturnKeyword
   264: 15,  #  RnmosKeyword
   265: 15,  #  RpmosKeyword
   266: 15,  #  RtranKeyword
   267: 15,  #  RtranIf0Keyword
   268: 15,  #  RtranIf1Keyword
   269: 15,  #  SAlwaysKeyword
   270: 15,  #  SEventuallyKeyword
   271: 15,  #  SNextTimeKeyword
   272: 15,  #  SUntilKeyword
   273: 15,  #  SUntilWithKeyword
   274: 15,  #  ScalaredKeyword
   275: 15,  #  SequenceKeyword
   276: 15,  #  ShortIntKeyword
   277: 15,  #  ShortRealKeyword
   278: 15,  #  ShowCancelledKeyword
   279: 15,  #  SignedKeyword
   280: 15,  #  SmallKeyword
   281: 15,  #  SoftKeyword
   282: 15,  #  SolveKeyword
   283: 15,  #  SpecifyKeyword
   284: 15,  #  SpecParamKeyword
   285: 15,  #  StaticKeyword
   286: 15,  #  StringKeyword
   287: 15,  #  StrongKeyword
   288: 15,  #  Strong0Keyword
   289: 15,  #  Strong1Keyword
   290: 15,  #  StructKeyword
   291: 15,  #  SuperKeyword
   292: 15,  #  Supply0Keyword
   293: 15,  #  Supply1Keyword
   294: 15,  #  SyncAcceptOnKeyword
   295: 15,  #  SyncRejectOnKeyword
   296: 15,  #  TableKeyword
   297: 15,  #  TaggedKeyword
   298: 15,  #  TaskKeyword
   299: 15,  #  ThisKeyword
   300: 15,  #  ThroughoutKeyword
   301: 15,  #  TimeKeyword
   302: 15,  #  TimePrecisionKeyword
   303: 15,  #  TimeUnitKeyword
   304: 15,  #  TranKeyword
   305: 15,  #  TranIf0Keyword
   306: 15,  #  TranIf1Keyword
   307: 15,  #  TriKeyword
   308: 15,  #  Tri0Keyword
   309: 15,  #  Tri1Keyword
   310: 15,  #  TriAndKeyword
   311: 15,  #  TriOrKeyword
   312: 15,  #  TriRegKeyword
   313: 15,  #  TypeKeyword
   314: 15,  #  TypedefKeyword
   315: 15,  #  UnionKeyword
   316: 15,  #  UniqueKeyword
   317: 15,  #  Unique0Keyword
   318: 15,  #  UnsignedKeyword
   319: 15,  #  UntilKeyword
   320: 15,  #  UntilWithKeyword
   321: 15,  #  UntypedKeyword
   322: 15,  #  UseKeyword
   323: 15,  #  UWireKeyword
   324: 15,  #  VarKeyword
   325: 15,  #  VectoredKeyword
   326: 15,  #  VirtualKeyword
   327: 15,  #  VoidKeyword
   328: 15,  #  WaitKeyword
   329: 15,  #  WaitOrderKeyword
   330: 15,  #  WAndKeyword
   331: 15,  #  WeakKeyword
   332: 15,  #  Weak0Keyword
   333: 15,  #  Weak1Keyword
   334: 15,  #  WhileKeyword
   335: 15,  #  WildcardKeyword
   336: 15,  #  WireKeyword
   337: 15,  #  WithKeyword
   338: 15,  #  WithinKeyword
   339: 15,  #  WOrKeyword
   340: 15,  #  XnorKeyword
   341: 15,  #  XorKeyword

   # predefined system keywords
   342: 15,  #  UnitSystemName
   343: 15,  #  RootSystemName

   # directives (these get consumed by the preprocessor and don't
   # make it downstream to the parser)
   344 : 14,  #  Directive
   345 : 14,  #  IncludeFileName
   346 : 14,  #  MacroUsage
   347 : 14,  #  MacroQuote
   348 : 14,  #  MacroEscapedQuote
   349 : 14,  #  MacroPaste
   350 : 14,  #  EmptyMacroArgument
   351 : 351  #  LineContinuation
}

tokenModifierMap = {

}

syntaxKindMap = {
   0   : 0,   # Unknown
   1   : 1,   # SyntaxList
   2   : 2,   # TokenList
   3   : 3,   # SeparatedList
   4   : 4,   # AcceptOnPropertyExpr
   5   : 5,   # ActionBlock
   6   : 6,   # AddAssignmentExpression
   7   : 7,   # AddExpression
   8   : 8,   # AlwaysBlock
   9   : 9,   # AlwaysCombBlock
   10  : 10,  # AlwaysFFBlock
   11  : 11,  # AlwaysLatchBlock
   12  : 12,  # AndAssignmentExpression
   13  : 13,  # AndPropertyExpr
   14  : 14,  # AndSequenceExpr
   15  : 15,  # AnsiPortList
   16  : 16,  # AnsiUdpPortList
   17  : 17,  # ArgumentList
   18  : 18,  # ArithmeticLeftShiftAssignmentExpression
   19  : 19,  # ArithmeticRightShiftAssignmentExpression
   20  : 20,  # ArithmeticShiftLeftExpression
   21  : 21,  # ArithmeticShiftRightExpression
   22  : 22,  # ArrayAndMethod
   23  : 23,  # ArrayOrMethod
   24  : 24,  # ArrayOrRandomizeMethodExpression
   25  : 25,  # ArrayUniqueMethod
   26  : 26,  # ArrayXorMethod
   27  : 27,  # AscendingRangeSelect
   28  : 28,  # AssertPropertyStatement
   29  : 29,  # AssertionItemPort
   30  : 30,  # AssertionItemPortList
   31  : 31,  # AssignmentExpression
   32  : 32,  # AssignmentPatternExpression
   33  : 33,  # AssignmentPatternItem
   34  : 34,  # AssumePropertyStatement
   35  : 35,  # AttributeInstance
   36  : 36,  # AttributeSpec
   37  : 37,  # BadExpression
   38  : 38,  # BeginKeywordsDirective
   39  : 39,  # BinaryAndExpression
   40  : 40,  # BinaryBinsSelectExpr
   41  : 41,  # BinaryBlockEventExpression
   42  : 42,  # BinaryEventExpression
   43  : 43,  # BinaryOrExpression
   44  : 44,  # BinaryXnorExpression
   45  : 45,  # BinaryXorExpression
   46  : 46,  # BindDirective
   47  : 47,  # BindTargetList
   48  : 48,  # BinsSelectConditionExpr
   49  : 49,  # BinsSelection
   50  : 50,  # BitSelect
   51  : 51,  # BitType
   52  : 52,  # BlockCoverageEvent
   53  : 53,  # BlockingEventTriggerStatement
   54  : 54,  # ByteType
   55  : 55,  # CHandleType
   56  : 56,  # CaseEqualityExpression
   57  : 57,  # CaseGenerate
   58  : 58,  # CaseInequalityExpression
   59  : 59,  # CasePropertyExpr
   60  : 60,  # CaseStatement
   61  : 61,  # CastExpression
   62  : 62,  # CellDefineDirective
   63  : 63,  # ChargeStrength
   64  : 64,  # CheckerDataDeclaration
   65  : 65,  # CheckerDeclaration
   66  : 66,  # CheckerInstanceStatement
   67  : 67,  # CheckerInstantiation
   68  : 68,  # ClassDeclaration
   69  : 69,  # ClassMethodDeclaration
   70  : 70,  # ClassMethodPrototype
   71  : 71,  # ClassName
   72  : 72,  # ClassPropertyDeclaration
   73  : 73,  # ClockingDeclaration
   74  : 74,  # ClockingDirection
   75  : 75,  # ClockingItem
   76  : 76,  # ClockingPropertyExpr
   77  : 77,  # ClockingSequenceExpr
   78  : 78,  # ClockingSkew
   79  : 79,  # ColonExpressionClause
   80  : 80,  # CompilationUnit
   81  : 81,  # ConcatenationExpression
   82  : 82,  # ConcurrentAssertionMember
   83  : 83,  # ConditionalConstraint
   84  : 84,  # ConditionalExpression
   85  : 85,  # ConditionalPathDeclaration
   86  : 86,  # ConditionalPattern
   87  : 87,  # ConditionalPredicate
   88  : 88,  # ConditionalPropertyExpr
   89  : 89,  # ConditionalStatement
   90  : 90,  # ConstraintBlock
   91  : 91,  # ConstraintDeclaration
   92  : 92,  # ConstraintPrototype
   93  : 93,  # ConstructorName
   94  : 94,  # ContinuousAssign
   95  : 95,  # CopyClassExpression
   96  : 96,  # CoverCross
   97  : 97,  # CoverPropertyStatement
   98  : 98,  # CoverSequenceStatement
   99  : 99,  # CoverageBins
   100 : 100, # CoverageIffClause
   101 : 101, # CoverageOption
   102 : 102, # CovergroupDeclaration
   103 : 103, # Coverpoint
   104 : 104, # CycleDelay
   105 : 105, # DPIExport
   106 : 106, # DPIImport
   107 : 107, # DataDeclaration
   108 : 108, # Declarator
   109 : 109, # DefParam
   110 : 110, # DefParamAssignment
   111 : 111, # DefaultCaseItem
   112 : 112, # DefaultClockingReference
   113 : 113, # DefaultCoverageBinInitializer
   114 : 114, # DefaultDisableDeclaration
   115 : 115, # DefaultNetTypeDirective
   116 : 116, # DefaultPatternKeyExpression
   117 : 117, # DefaultPropertyCaseItem
   118 : 118, # DefaultRsCaseItem
   119 : 119, # DefaultSkewItem
   120 : 120, # DeferredAssertion
   121 : 121, # DefineDirective
   122 : 122, # Delay3
   123 : 123, # DelayControl
   124 : 124, # DelayedSequenceElement
   125 : 125, # DelayedSequenceExpr
   126 : 126, # DelayedTerminalArg
   127 : 127, # DescendingRangeSelect
   128 : 128, # DisableConstraint
   129 : 129, # DisableForkStatement
   130 : 130, # DisableIff
   131 : 131, # DisableStatement
   132 : 132, # DistConstraintList
   133 : 133, # DistItem
   134 : 134, # DistWeight
   135 : 135, # DivideAssignmentExpression
   136 : 136, # DivideExpression
   137 : 137, # DividerClause
   138 : 138, # DoWhileStatement
   139 : 139, # DotMemberClause
   140 : 140, # DriveStrength
   141 : 141, # EdgeControlSpecifier
   142 : 142, # EdgeDescriptor
   143 : 143, # EdgeSensitivePathSuffix
   144 : 144, # ElabSystemTask
   145 : 145, # ElementSelect
   146 : 146, # ElementSelectExpression
   147 : 147, # ElsIfDirective
   148 : 148, # ElseClause
   149 : 149, # ElseConstraintClause
   150 : 150, # ElseDirective
   151 : 151, # ElsePropertyClause
   152 : 152, # EmptyArgument
   153 : 153, # EmptyIdentifierName
   154 : 154, # EmptyMember
   155 : 155, # EmptyNonAnsiPort
   156 : 156, # EmptyPortConnection
   157 : 157, # EmptyQueueExpression
   158 : 158, # EmptyStatement
   159 : 159, # EmptyTimingCheckArg
   160 : 160, # EndCellDefineDirective
   161 : 161, # EndIfDirective
   162 : 162, # EndKeywordsDirective
   163 : 163, # EnumType
   164 : 164, # EqualityExpression
   165 : 165, # EqualsAssertionArgClause
   166 : 166, # EqualsTypeClause
   167 : 167, # EqualsValueClause
   168 : 168, # EventControl
   169 : 169, # EventControlWithExpression
   170 : 170, # EventType
   171 : 171, # ExpectPropertyStatement
   172 : 172, # ExplicitAnsiPort
   173 : 173, # ExplicitNonAnsiPort
   174 : 174, # ExpressionConstraint
   175 : 175, # ExpressionCoverageBinInitializer
   176 : 176, # ExpressionOrDist
   177 : 177, # ExpressionPattern
   178 : 178, # ExpressionStatement
   179 : 179, # ExpressionTimingCheckArg
   180 : 180, # ExtendsClause
   181 : 181, # ExternModule
   182 : 182, # FinalBlock
   183 : 183, # FirstMatchSequenceExpr
   184 : 184, # FollowedByPropertyExpr
   185 : 185, # ForLoopStatement
   186 : 186, # ForVariableDeclaration
   187 : 187, # ForeachLoopList
   188 : 188, # ForeachLoopStatement
   189 : 189, # ForeverStatement
   190 : 190, # ForwardInterfaceClassTypedefDeclaration
   191 : 191, # ForwardTypedefDeclaration
   192 : 192, # FunctionDeclaration
   193 : 193, # FunctionPort
   194 : 194, # FunctionPortList
   195 : 195, # FunctionPrototype
   196 : 196, # GenerateBlock
   197 : 197, # GenerateRegion
   198 : 198, # GenvarDeclaration
   199 : 199, # GreaterThanEqualExpression
   200 : 200, # GreaterThanExpression
   201 : 201, # HierarchicalInstance
   202 : 202, # HierarchyInstantiation
   203 : 203, # IdentifierName
   204 : 204, # IdentifierSelectName
   205 : 205, # IfDefDirective
   206 : 206, # IfGenerate
   207 : 207, # IfNDefDirective
   208 : 208, # IfNonePathDeclaration
   209 : 209, # IffEventClause
   210 : 210, # IffPropertyExpr
   211 : 211, # ImmediateAssertStatement
   212 : 212, # ImmediateAssertionMember
   213 : 213, # ImmediateAssumeStatement
   214 : 214, # ImmediateCoverStatement
   215 : 215, # ImplementsClause
   216 : 216, # ImplicationConstraint
   217 : 217, # ImplicationPropertyExpr
   218 : 218, # ImplicitAnsiPort
   219 : 219, # ImplicitEventControl
   220 : 220, # ImplicitNonAnsiPort
   221 : 221, # ImplicitType
   222 : 222, # ImpliesPropertyExpr
   223 : 223, # IncludeDirective
   224 : 224, # InequalityExpression
   225 : 225, # InitialBlock
   226 : 226, # InsideExpression
   227 : 227, # InstanceName
   228 : 228, # IntType
   229 : 229, # IntegerLiteralExpression
   230 : 230, # IntegerType
   231 : 231, # IntegerVectorExpression
   232 : 232, # InterfaceDeclaration
   233 : 233, # InterfaceHeader
   234 : 234, # InterfacePortHeader
   235 : 235, # IntersectClause
   236 : 236, # IntersectSequenceExpr
   237 : 237, # InvocationExpression
   238 : 238, # JumpStatement
   239 : 239, # LessThanEqualExpression
   240 : 240, # LessThanExpression
   241 : 241, # LetDeclaration
   242 : 242, # LineDirective
   243 : 243, # LocalScope
   244 : 244, # LocalVariableDeclaration
   245 : 245, # LogicType
   246 : 246, # LogicalAndExpression
   247 : 247, # LogicalEquivalenceExpression
   248 : 248, # LogicalImplicationExpression
   249 : 249, # LogicalLeftShiftAssignmentExpression
   250 : 250, # LogicalOrExpression
   251 : 251, # LogicalRightShiftAssignmentExpression
   252 : 252, # LogicalShiftLeftExpression
   253 : 253, # LogicalShiftRightExpression
   254 : 254, # LongIntType
   255 : 255, # LoopConstraint
   256 : 256, # LoopGenerate
   257 : 257, # LoopStatement
   258 : 258, # MacroActualArgument
   259 : 259, # MacroActualArgumentList
   260 : 260, # MacroArgumentDefault
   261 : 261, # MacroFormalArgument
   262 : 262, # MacroFormalArgumentList
   263 : 263, # MacroUsage
   264 : 264, # MatchesClause
   265 : 265, # MemberAccessExpression
   266 : 266, # MinTypMaxExpression
   267 : 267, # ModAssignmentExpression
   268 : 268, # ModExpression
   269 : 269, # ModportClockingPort
   270 : 270, # ModportDeclaration
   271 : 271, # ModportExplicitPort
   272 : 272, # ModportItem
   273 : 273, # ModportNamedPort
   274 : 274, # ModportSimplePortList
   275 : 275, # ModportSubroutinePort
   276 : 276, # ModportSubroutinePortList
   277 : 277, # ModuleDeclaration
   278 : 278, # ModuleHeader
   279 : 279, # MultipleConcatenationExpression
   280 : 280, # MultiplyAssignmentExpression
   281 : 281, # MultiplyExpression
   282 : 282, # NameValuePragmaExpression
   283 : 283, # NamedArgument
   284 : 284, # NamedBlockClause
   285 : 285, # NamedLabel
   286 : 286, # NamedParamAssignment
   287 : 287, # NamedPortConnection
   288 : 288, # NamedStructurePatternMember
   289 : 289, # NamedType
   290 : 290, # NetAlias
   291 : 291, # NetDeclaration
   292 : 292, # NetPortHeader
   293 : 293, # NetTypeDeclaration
   294 : 294, # NewArrayExpression
   295 : 295, # NewClassExpression
   296 : 296, # NoUnconnectedDriveDirective
   297 : 297, # NonAnsiPortList
   298 : 298, # NonAnsiUdpPortList
   299 : 299, # NonblockingAssignmentExpression
   300 : 300, # NonblockingEventTriggerStatement
   301 : 301, # NullLiteralExpression
   302 : 302, # NumberPragmaExpression
   303 : 303, # OneStepDelay
   304 : 304, # OpenRangeExpression
   305 : 305, # OpenRangeList
   306 : 306, # OrAssignmentExpression
   307 : 307, # OrPropertyExpr
   308 : 308, # OrSequenceExpr
   309 : 309, # OrderedArgument
   310 : 310, # OrderedParamAssignment
   311 : 311, # OrderedPortConnection
   312 : 312, # OrderedStructurePatternMember
   313 : 313, # PackageDeclaration
   314 : 314, # PackageExportAllDeclaration
   315 : 315, # PackageExportDeclaration
   316 : 316, # PackageHeader
   317 : 317, # PackageImportDeclaration
   318 : 318, # PackageImportItem
   319 : 319, # ParallelBlockStatement
   320 : 320, # ParameterDeclaration
   321 : 321, # ParameterDeclarationStatement
   322 : 322, # ParameterPortList
   323 : 323, # ParameterValueAssignment
   324 : 324, # ParenExpressionList
   325 : 325, # ParenPragmaExpression
   326 : 326, # ParenthesizedBinsSelectExpr
   327 : 327, # ParenthesizedEventExpression
   328 : 328, # ParenthesizedExpression
   329 : 329, # ParenthesizedPattern
   330 : 330, # ParenthesizedPropertyExpr
   331 : 331, # ParenthesizedSequenceExpr
   332 : 332, # PathDeclaration
   333 : 333, # PathDescription
   334 : 334, # PatternCaseItem
   335 : 335, # PortConcatenation
   336 : 336, # PortDeclaration
   337 : 337, # PortReference
   338 : 338, # PostdecrementExpression
   339 : 339, # PostincrementExpression
   340 : 340, # PowerExpression
   341 : 341, # PragmaDirective
   342 : 342, # PrimaryBlockEventExpression
   343 : 343, # PrimitiveInstantiation
   344 : 344, # ProceduralAssignStatement
   345 : 345, # ProceduralDeassignStatement
   346 : 346, # ProceduralForceStatement
   347 : 347, # ProceduralReleaseStatement
   348 : 348, # Production
   349 : 349, # ProgramDeclaration
   350 : 350, # ProgramHeader
   351 : 351, # PropertyDeclaration
   352 : 352, # PropertySpec
   353 : 353, # PropertyType
   354 : 354, # PullStrength
   355 : 355, # PulseStyleDeclaration
   356 : 356, # QueueDimensionSpecifier
   357 : 357, # RandCaseItem
   358 : 358, # RandCaseStatement
   359 : 359, # RandJoinClause
   360 : 360, # RandSequenceStatement
   361 : 361, # RangeCoverageBinInitializer
   362 : 362, # RangeDimensionSpecifier
   363 : 363, # RealLiteralExpression
   364 : 364, # RealTimeType
   365 : 365, # RealType
   366 : 366, # RegType
   367 : 367, # RepeatedEventControl
   368 : 368, # ReplicatedAssignmentPattern
   369 : 369, # ResetAllDirective
   370 : 370, # RestrictPropertyStatement
   371 : 371, # ReturnStatement
   372 : 372, # RootScope
   373 : 373, # RsCase
   374 : 374, # RsCodeBlock
   375 : 375, # RsElseClause
   376 : 376, # RsIfElse
   377 : 377, # RsProdItem
   378 : 378, # RsRepeat
   379 : 379, # RsRule
   380 : 380, # RsWeightClause
   381 : 381, # SUntilPropertyExpr
   382 : 382, # SUntilWithPropertyExpr
   383 : 383, # ScopedName
   384 : 384, # SequenceDeclaration
   385 : 385, # SequenceMatchList
   386 : 386, # SequenceRepetition
   387 : 387, # SequenceType
   388 : 388, # SequentialBlockStatement
   389 : 389, # ShortIntType
   390 : 390, # ShortRealType
   391 : 391, # SignalEventExpression
   392 : 392, # SignedCastExpression
   393 : 393, # SimpleAssignmentPattern
   394 : 394, # SimpleBinsSelectExpr
   395 : 395, # SimplePathSuffix
   396 : 396, # SimplePragmaExpression
   397 : 397, # SimplePropertyExpr
   398 : 398, # SimpleRangeSelect
   399 : 399, # SimpleSequenceExpr
   400 : 400, # SolveBeforeConstraint
   401 : 401, # SpecifyBlock
   402 : 402, # SpecparamDeclaration
   403 : 403, # SpecparamDeclarator
   404 : 404, # StandardCaseItem
   405 : 405, # StandardPropertyCaseItem
   406 : 406, # StandardRsCaseItem
   407 : 407, # StreamExpression
   408 : 408, # StreamExpressionWithRange
   409 : 409, # StreamingConcatenationExpression
   410 : 410, # StringLiteralExpression
   411 : 411, # StringType
   412 : 412, # StrongWeakPropertyExpr
   413 : 413, # StructType
   414 : 414, # StructUnionMember
   415 : 415, # StructurePattern
   416 : 416, # StructuredAssignmentPattern
   417 : 417, # SubtractAssignmentExpression
   418 : 418, # SubtractExpression
   419 : 419, # SuperHandle
   420 : 420, # SystemName
   421 : 421, # SystemTimingCheck
   422 : 422, # TaggedPattern
   423 : 423, # TaggedUnionExpression
   424 : 424, # TaskDeclaration
   425 : 425, # ThisHandle
   426 : 426, # ThroughoutSequenceExpr
   427 : 427, # TimeLiteralExpression
   428 : 428, # TimeScaleDirective
   429 : 429, # TimeType
   430 : 430, # TimeUnitsDeclaration
   431 : 431, # TimingCheckCondition
   432 : 432, # TimingCheckEvent
   433 : 433, # TimingControlExpression
   434 : 434, # TimingControlStatement
   435 : 435, # TransListCoverageBinInitializer
   436 : 436, # TransRange
   437 : 437, # TransRepeatRange
   438 : 438, # TransSet
   439 : 439, # TypeAssignment
   440 : 440, # TypeParameterDeclaration
   441 : 441, # TypeReference
   442 : 442, # TypedefDeclaration
   443 : 443, # UdpBody
   444 : 444, # UdpDeclaration
   445 : 445, # UdpEdgeIndicator
   446 : 446, # UdpEntry
   447 : 447, # UdpInitialStmt
   448 : 448, # UdpInputPortDecl
   449 : 449, # UdpOutputPortDecl
   450 : 450, # UnaryBinsSelectExpr
   451 : 451, # UnaryBitwiseAndExpression
   452 : 452, # UnaryBitwiseNandExpression
   453 : 453, # UnaryBitwiseNorExpression
   454 : 454, # UnaryBitwiseNotExpression
   455 : 455, # UnaryBitwiseOrExpression
   456 : 456, # UnaryBitwiseXnorExpression
   457 : 457, # UnaryBitwiseXorExpression
   458 : 458, # UnaryLogicalNotExpression
   459 : 459, # UnaryMinusExpression
   460 : 460, # UnaryPlusExpression
   461 : 461, # UnaryPredecrementExpression
   462 : 462, # UnaryPreincrementExpression
   463 : 463, # UnaryPropertyExpr
   464 : 464, # UnarySelectPropertyExpr
   465 : 465, # UnbasedUnsizedLiteralExpression
   466 : 466, # UnconnectedDriveDirective
   467 : 467, # UndefDirective
   468 : 468, # UndefineAllDirective
   469 : 469, # UnionType
   470 : 470, # UniquenessConstraint
   471 : 471, # UnitScope
   472 : 472, # UntilPropertyExpr
   473 : 473, # UntilWithPropertyExpr
   474 : 474, # Untyped
   475 : 475, # UserDefinedNetDeclaration
   476 : 476, # VariableDimension
   477 : 477, # VariablePattern
   478 : 478, # VariablePortHeader
   479 : 479, # VirtualInterfaceType
   480 : 480, # VoidCastedCallStatement
   481 : 481, # VoidType
   482 : 482, # WaitForkStatement
   483 : 483, # WaitOrderStatement
   484 : 484, # WaitStatement
   485 : 485, # WildcardDimensionSpecifier
   486 : 486, # WildcardEqualityExpression
   487 : 487, # WildcardInequalityExpression
   488 : 488, # WildcardLiteralExpression
   489 : 489, # WildcardPattern
   490 : 490, # WildcardPortConnection
   491 : 491, # WildcardPortList
   492 : 492, # WildcardUdpPortList
   493 : 493, # WithClause
   494 : 494, # WithFunctionClause
   495 : 495, # WithFunctionSample
   496 : 496, # WithinSequenceExpr
   497 : 497, # XorAssignmentExpression
}