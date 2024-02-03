`timescale 1ns / 1ns

module testbench();

reg X, Y, clk, reset;
wire [3:0] Z;

source testCircuit(X, Y, clk, Z, reset);

initial begin
	$dumpfile("TimingDiagram.vcd");
	$dumpvars(0, testCircuit, X, Y, clk, Z, reset);
	reset=0; X=0; Y=0; clk=0;
	#20;
	reset=0; X=0; Y=0; clk=1;
	#20;
	reset=0; X=0; Y=1; clk=0;
	#20;
	reset=0; X=0; Y=1; clk=1;
	#20;
	reset=0; X=1; Y=0; clk=0;
	#20;
	reset=0; X=1; Y=0; clk=1;
	#20;
	reset=0; X=1; Y=1; clk=0;
	#20;
	reset=0; X=1; Y=1; clk=1;
	#20;
	
	$finish;
end

endmodule
