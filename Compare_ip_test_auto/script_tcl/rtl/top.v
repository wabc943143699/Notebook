module top
(
    input clk,
    input rst_n,
    input en,
    input i_d,
    output reg o_q
);

always@(posedge clk or negedge rst_n)begin
    if(!rst_n)begin
        o_q<=0;
    end    
    else if(en) begin
       o_q<=i_d; 
    end
end

endmodule