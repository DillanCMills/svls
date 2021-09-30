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

struct debugFoo {
public:

   Compilation comp;
   SourceManager sm;
   std::shared_ptr<SyntaxTree> t = SyntaxTree::fromText(R"(
   module foo #(parameter int i) (
   input logic clk
   );
   logic [5:0] bar;

   always_ff @(posedge clk) begin
      bar += 1'b1;
   end

   endmodule: foo
   )", sm);

   // Diagnostics& diags;
   // RootSymbol& root;
   // InstanceSymbol& elem;
   // InstanceBodySymbol body;

   const InstanceBodySymbol& setup() {
      this->comp.addSyntaxTree(t);

      auto& diags = comp.getAllDiagnostics();

      auto& root = comp.getRoot();
      auto& elem = (root.members()[1])->as<InstanceSymbol>();
      const auto& body = elem.body;

      return body;
   }

};