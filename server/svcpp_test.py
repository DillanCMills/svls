from .svcpp import *
# cppyy.set_debug()

comp = Compilation()
sm = SourceManager()
t = SyntaxTree.fromText('''module foo;
   logic [5:0] bar;

   always_ff @(posedge clk) begin
      bar += 1'b1;
   end

endmodule: foo
   ''', sm)

comp.addSyntaxTree(t)
de = DiagnosticEngine(t.sourceManager())
client = JSONDiagnosticClient()
de.addClient(client)

for d in comp.getAllDiagnostics():
   de.issue(d)

results = client.getBuf()

nr = Visitor()
nr.walkTree(t.root())
# nr.visit(t.root())

# t.root().visit(nr)
# print(nr.count)