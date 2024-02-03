`timescale 1ns/1ns
module FSM_Testbench();

wire y;
reg x;
reg rst;
reg clk;
parameter inputsequence1 = 32'b00110001101111101000010101111000, 
	inputsequence2 = 32'b00000010000011100001100000011001,
	inputsequence3 = 32'b11100100000110111100001111111000,
	inputsequence4 = 32'b00010010111011111010000101000011,
	inputsequence5 = 32'b11111111000111000001010011010000;

integer i;

FSM fsm(y, x, clk, rst);

initial begin
    $dumpfile("TimingDiagram.vcd");
    $dumpvars(0, y, x, rst, clk, fsm);
    
    rst = 1;
    x = 0;
    #30;
    rst = 0;
    
    for (i=31; i>=0; i--) begin
        x = inputsequence1[i]; // Change this to check other cases
        #40;
    end
    
    $finish;
end

always begin	
	clk = 0;
	#20;
	clk = 1;
	#20;
end

endmodule
