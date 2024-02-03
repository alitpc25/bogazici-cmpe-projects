`timescale 1ns / 1ns
module TestBench();

reg i2, i1, i0;
wire o;

source my_module(i2, i1, i0, o);

initial begin
	$dumpfile("TimingDiagram.vcd");
	$dumpvars(0, i2, i1, i0, o);
	
	i2 = 0; i1 = 0; i0 = 0;
	#20
	i2 = 0; i1 = 0; i0 = 1;
	#20
	i2 = 0; i1 = 1; i0 = 0;
	#20
	i2 = 0; i1 = 1; i0 = 1;
	#20
	i2 = 1; i1 = 0; i0 = 0;
	#20
	i2 = 1; i1 = 0; i0 = 1;
	#20
	i2 = 1; i1 = 1; i0 = 0;
	#20
	i2 = 1; i1 = 1; i0 = 1;
	#20
	
	$finish;
end

endmodule
