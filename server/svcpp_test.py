from .svcpp import *
# cppyy.set_debug()

comp = Compilation()
sm = SourceManager()
t = SyntaxTree.fromFile('server/test.sv', sm)
# t = SyntaxTree.fromText('''module foo;
#    logic [5:0] bar;

#    always_ff @(posedge clk) begin
#       bar += 1'b1;
#    end

# endmodule: foo
# ''', sm)

comp.addSyntaxTree(t)
de = DiagnosticEngine(t.sourceManager())
client = JSONDiagnosticClient()
de.addClient(client)

for d in comp.getAllDiagnostics():
   de.issue(d)

results = client.getBuf()

v = Visitor(comp, sm)
# nr.walkTree(t.root())
# nr.visit(t.root())

# t.root().visit(nr)
# print(nr.count)


# from server.svcpp_test import *
x = comp.getRoot()
writer = JsonWriter()
writer.setPrettyPrint(True)
writer.setIndentSize(2)
serializer = ASTSerializer(comp, writer)
serializer.serialize(comp.getRoot())
print(writer.view())

# x = comp.getRoot().getLastMember()
# y = bind_object(x, InstanceSymbol)
# z = y.body
# str(z.name)

root = comp.getRoot()
elem = bind_object(root.members()[1].__deref__(), slang.InstanceSymbol)
body = elem.body
param = bind_object(body.members()[0].__deref__(), slang.ParameterSymbol)
port0 = bind_object(body.members()[1].__deref__(), slang.PortSymbol)
var0 = bind_object(body.members()[2].__deref__(), slang.VariableSymbol)
port1 = bind_object(body.members()[3].__deref__(), slang.PortSymbol)
var1 = bind_object(body.members()[4].__deref__(), slang.VariableSymbol)
var2 = bind_object(body.members()[5].__deref__(), slang.VariableSymbol)
alw = bind_object(body.members()[6].__deref__(), slang.ProceduralBlockSymbol)
stmt = bind_object(alw.getBody(), slang.TimedStatement)
timing = stmt.timing
timingList = bind_object(timing, slang.EventListControl)
t0 = bind_object(timingList.events[0], slang.SignalEventControl)
t1 = bind_object(timingList.events[1], slang.SignalEventControl)
block = bind_object(stmt.stmt, slang.BlockStatement)
lst = bind_object(block.getStatements(), slang.StatementList)
expr = bind_object(lst.list[0], slang.ExpressionStatement)
assign = bind_object(expr.expr, slang.AssignmentExpression)

v.walkDesignTree(comp.getRoot())
for x in v.tokens:
   print(x)

# print(body.name)

# cppyy.cppdef('''
# #include <iostream>
# #include "slang/syntax/SyntaxTree.h"
# #include "slang/compilation/Compilation.h"
# #include "slang/text/SourceManager.h"
# #include "slang/diagnostics/DiagnosticEngine.h"
# #include "slang/diagnostics/TextDiagnosticClient.h"
# #include "slang/text/Json.h"
# #include "slang/symbols/ASTSerializer.h"
# #include "slang/symbols/CompilationUnitSymbols.h"
# #include "slang/compilation/DesignTree.h"
# #include "slang/symbols/InstanceSymbols.h"

# using namespace slang;

# struct debugFoo {
# public:

#    Compilation comp;
#    SourceManager sm;
#    std::shared_ptr<SyntaxTree> t = SyntaxTree::fromText(R"(
#    module foo #(parameter int i) (
#    input logic clk
#    );
#    logic [5:0] bar;

#    always_ff @(posedge clk) begin
#       bar += 1'b1;
#    end

#    endmodule: foo
#    )", sm);

#    // Diagnostics& diags;
#    // RootSymbol& root;
#    // InstanceSymbol& elem;
#    // InstanceBodySymbol body;

#    const InstanceBodySymbol& setup() {
#       comp.addSyntaxTree(t);

#       auto& diags = comp.getAllDiagnostics();

#       auto& root = comp.getRoot();
#       auto& elem = (root.members()[1])->as<InstanceSymbol>();
#       const auto& body = elem.body;

#       return body;
#    }

# };
# ''')