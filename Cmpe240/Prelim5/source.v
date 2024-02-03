`timescale 1ns / 1ns

module FSM (y, x, clk, rst);

output reg y;
input wire x;
input wire rst;
input wire clk;

parameter S0 = 7'b0000001,
	S1 = 7'b0000010,
	S2 = 7'b0000100,
	S3 = 7'b0001000,
	S4 = 7'b0010000,
	S5 = 7'b0100000,
	S6 = 7'b1000000;
	
	
reg [6:0] stateReg;
reg [6:0] nextStateReg;

always@(x, stateReg) begin
	case(stateReg)
		S0: begin
			if(x == 0) begin
				nextStateReg <= S4;
			end
			else begin
				nextStateReg <= S1;
			end
			y <= 1'b0;
		end
		S1: begin
			if(x == 0) begin
				nextStateReg <= S4;
			end
			else begin
				nextStateReg <= S2;
			end
			y <= 1'b0;
		end
		S2: begin
			if(x == 0) begin
				nextStateReg <= S4;
			end
			else begin
				nextStateReg <= S3;
			end
			y <= 1'b0;
		end
		S3: begin
			if(x == 0) begin
				nextStateReg <= S4;
			end
			else begin
				nextStateReg <= S3;
			end
			y <= 1'b1;
		end
		S4: begin
			if(x == 0) begin
				nextStateReg <= S5;
			end
			else begin
				nextStateReg <= S1;
			end
			y <= 1'b0;
		end
		S5: begin
			if(x == 0) begin
				nextStateReg <= S6;
			end
			else begin
				nextStateReg <= S1;
			end
			y <= 1'b0;
		end
		S6: begin
			if(x == 0) begin
				nextStateReg <= S6;
			end
			else begin
				nextStateReg <= S1;
			end
			y <= 1'b1;
		end
	endcase
end

always@(posedge clk) begin
	if(rst) begin
		stateReg <= S0;
	end
	else begin
		stateReg <= nextStateReg;
	end
end

endmodule
	