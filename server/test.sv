module foo #(parameter int i) (
   input logic clk,
   input logic rst_n
);
   logic [5:0] bar;

   always_ff @(posedge clk or negedge rst_n) begin
      bar += 1'b1;
   end

endmodule: foo