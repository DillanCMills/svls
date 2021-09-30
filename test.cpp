#include <iostream>
#include "slang/syntax/SyntaxTree.h"
#include "slang/compilation/Compilation.h"
#include "slang/text/SourceManager.h"
#include "slang/diagnostics/DiagnosticEngine.h"
#include "slang/diagnostics/TextDiagnosticClient.h"
#include "slang/text/Json.h"
#include "slang/symbols/ASTSerializer.h"
#include "slang/symbols/CompilationUnitSymbols.h"
#include "slang/compilation/DesignTree.h"
#include "slang/symbols/InstanceSymbols.h"

using namespace slang;

int main (void) {
   Compilation comp;
   SourceManager sm;
   auto t = SyntaxTree::fromText(R"(
module foo #(parameter int i) (
   input logic clk
);
   logic [5:0] bar;

   always_ff @(posedge clk) begin
      bar += 1'b1;
   end

endmodule: foo
)", sm);
   comp.addSyntaxTree(t);
   // auto de = DiagnosticEngine(t->sourceManager());
   // auto dc = std::make_shared<TextDiagnosticClient>();
   // de.addClient(dc);

   // for (auto& d : comp.getAllDiagnostics())
   //    de.issue(d);

   // std::cout << dc->getString() << '\n';

   auto& diags = comp.getAllDiagnostics();
   if (!diags.empty()) {
      std::cout << "Diagnostics reported\n";
   }

   JsonWriter writer;
   writer.setPrettyPrint(true);
   writer.setIndentSize(2);
   ASTSerializer serializer(comp, writer);
   serializer.serialize(comp.getRoot());
   
   std::cout << writer.view() << '\n';

   // auto x = comp.getDesignTree().childNodes[0];
   // auto y = x->instance;
   // auto z = &y->body;

   // std::cout << z->name << '\n';

   // auto dt = &comp.getDesignTree();
   // auto top = dt->childNodes[0];
   // std::cout << top->symbol.name << '\n';

   auto& root = comp.getRoot();
   auto& elem = root.members()[1]->cast<InstanceSymbol>();
   auto& body = elem.body;

   std::cout << body.name << '\n';

   std::cout << "Sanity Check\n";
   
   return 0;
}

// clang++-11 -L ./external/slang/build/lib/ -I ./external/slang/include -I ./external/slang/external -I ./external/slang/build/source -std=c++17 -Wall -o test test.cpp -lslangcore -lslangparser -lslangruntime -lslangcompiler -g
// LD_LIBRARY_PATH=./external/slang/build/lib/ ./test