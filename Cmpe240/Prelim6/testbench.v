`timescale 1ns/1ns
module RTL_Testbench();

wire [3:0] max_index;
wire completed;

reg start;
reg clk;
reg reset;

wire update_max, index_lt_eight, index_ld, index_clr, max_ld, max_clr, max_index_ld, max_index_clr, completed_ld, completed_clr;

reg [63:0] input_array;

RTL_Controller controller (start, clk, reset, update_max, index_lt_eight, index_ld, index_clr, max_ld, max_clr, max_index_ld, max_index_clr, completed_ld, completed_clr);
RTL_Datapath datapath (max_index, completed, clk, reset, input_array, update_max, index_lt_eight, index_ld, index_clr, max_ld, max_clr, max_index_ld, max_index_clr, completed_ld, completed_clr);

initial begin
    $dumpfile("TimingDiagram.vcd");
    $dumpvars(0, input_array, start, clk, reset, max_index, completed, controller,datapath,update_max, index_lt_eight, index_ld, index_clr, max_ld, max_clr, max_index_ld, max_index_clr, completed_ld, completed_clr);
	
    input_array = 64'b1000000000000000100000010000000110000010000000101000001100000011;
    reset = 1'b1;
    start = 1'b0;
    #30;
    reset = 1'b0;
    start = 1'b1;
	#40;
	start = 1'b0;
	#1200;
    
    $finish;
end

always begin	
	clk = 0;
	#20;
	clk = 1;
	#20;
end

endmodule
