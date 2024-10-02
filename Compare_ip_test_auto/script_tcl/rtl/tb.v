`timescale 1ns/100ps
module tb();

reg clk;
reg rst_n;
reg en;
reg i_d;
wire o_q;
integer fp;
initial begin
    fp = $fopen("D:/Code/vivado/script_tcl/my_project_dir/data_out.txt","w");
end
initial begin
    clk<=0;
    rst_n<=0;
    en<=0;
    i_d<=0;
    #100;
    rst_n<=1;
    #50
    en<=1;
    #50;
    repeat(50)begin
        i_d<=$random;
        
        #20;
    end
    $fclose(fp);
    $finish;
end
always@(posedge clk)begin
    if(en)begin
        $fwrite(fp,"%d\n",i_d);
    end
end
always #10 clk<=~clk;
top u_top(.clk(clk),.rst_n(rst_n),.en(en),.i_d(i_d),.o_q(o_q));
endmodule