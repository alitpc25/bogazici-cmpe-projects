
module decoder2to4(F3, F2, F1, F0, D, E);

output reg F3, F2, F1, F0;
input D, E;

always @(D or E) begin
	case ({D,E})
		2'b00: {F3, F2, F1, F0} = ~4'b1110;
		2'b01: {F3, F2, F1, F0} = ~4'b1101;
		2'b10: {F3, F2, F1, F0} = ~4'b1011;
		2'b11: {F3, F2, F1, F0} = ~4'b0111;
		default: {F3, F2, F1, F0} = 4'bxxxx;
	endcase
end

endmodule

module mux8to1(Z, I7, I6, I5, I4, I3, I2, I1, I0, A, B, C);

output reg Z;
input I7, I6, I5, I4, I3, I2, I1, I0;
input A, B, C;

always @(I7, I6, I5, I4, I3, I2, I1, I0, A, B, C) begin
	case ({A, B, C})
		3'b000: Z <= I0;
		3'b001: Z <= I1;
		3'b010: Z <= I2;
		3'b011: Z <= I3;
		3'b100: Z <= I4;
		3'b101: Z <= I5;
		3'b110: Z <= I6;
		3'b111: Z <= I7;
		default: Z <= 3'bxxx;
	endcase
end

endmodule



module source(Y, A, B, C, D, E);

output Y;
input A, B, C, D, E;

wire F3, F2, F1, F0;
wire notD;
wire notDplusEprime;

not(notD, D);
decoder2to4 decoder(F3, F2, F1, F0, D, E);
not(notDplusEprime, F1);
not(notDprimePlusE, F2);
mux8to1 mux(Y, notDprimePlusE, notD, F1, notDplusEprime, F1, F1, F2, D, A, B, C);

endmodule