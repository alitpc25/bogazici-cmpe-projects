module DFlipFlop (Q, D, clk, reset);

output reg Q;
input D, clk, reset;

always @(posedge clk)
begin
	if(reset)
	begin
		Q <= 0;
	end
	else
	begin
		Q <= D;
	end
end

endmodule


module source(X, Y, clk, Z, reset);

input X, Y, clk, reset;
output [3:0] Z;
wire s1, s0;

wire s1s0;
wire s1primes0;
wire s1s0prime;
wire nots1;
wire nots0;
wire s1primes0ORs1s0prime;

DFlipFlop dflipflop1(s1, X, clk, reset);
DFlipFlop dflipflop2(s0, Y, clk, reset);

not(nots1, s1);
not(nots0, s0);

and(s1s0, s1, s0);
and(s1primes0, nots1, s0);
and(s1s0prime, s1, nots0);
or(s1primes0ORs1s0prime, s1primes0, s1s0prime);

assign Z = {s1s0, s1s0prime, s1primes0ORs1s0prime, s0};

endmodule
