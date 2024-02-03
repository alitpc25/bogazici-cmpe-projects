`timescale 1ns / 1ns
module RTL_Controller(start, clk, reset, update_max, index_lt_eight, index_ld, index_clr, max_ld, max_clr, max_index_ld, max_index_clr, completed_ld, completed_clr);

input start, clk, reset, update_max, index_lt_eight;
output reg index_ld, index_clr, max_ld, max_clr, max_index_ld, max_index_clr, completed_ld, completed_clr;

parameter Reset = 3'b000,
	Init = 3'b001,
	Compare = 3'b010,
	NewMax = 3'b011,
	IncreaseIndex = 3'b100,
	Finish = 3'b101;
	
reg [2:0] state, nextState;

always@(state,start,update_max, index_lt_eight) begin
	case(state)
		Reset: begin
			if(start == 1'b1) begin
				nextState <= Init;
			end
			else begin
				nextState <= Reset;
			end
			
			max_clr <= 1'b1;
			index_clr <= 1'b1;
			max_index_clr <= 1'b1;
			
			completed_ld <= 1'b0;
			completed_clr <= 1'b1;
			index_ld <= 1'b0;
			max_ld <= 1'b0;
			max_index_ld <= 1'b0;
		end
		Init: begin
			nextState <= Compare;
			
			max_clr <= 1'b0;
			index_clr <= 1'b0;
			max_index_clr <= 1'b0;
			
			completed_ld <= 1'b0;
			completed_clr <= 1'b0;
			index_ld <= 1'b0;
			max_ld <= 1'b0;
			max_index_ld <= 1'b0;
		end
		Compare: begin
			if(update_max == 1) begin
				nextState <= NewMax;
			end
			else begin
				nextState <= IncreaseIndex;
			end
			
			max_clr <= 1'b0;
			index_clr <= 1'b0;
			max_index_clr <= 1'b0;
			
			completed_ld <= 1'b0;
			completed_clr <= 1'b0;
			index_ld <= 1'b0;
			max_ld <= 1'b0;
			max_index_ld <= 1'b0;
		end
		NewMax: begin
			nextState <= IncreaseIndex;
			
			max_clr <= 1'b0;
			index_clr <= 1'b0;
			max_index_clr <= 1'b0;
			
			completed_ld <= 1'b0;
			completed_clr <= 1'b0;
			index_ld <= 1'b0;
			max_ld <= 1'b1;
			max_index_ld <= 1'b1;
		end
		IncreaseIndex: begin
			if(index_lt_eight == 1) begin
				nextState <= Compare;
			end
			else begin
				nextState <= Finish;
			end
			
			max_clr <= 1'b0;
			index_clr <= 1'b0;
			max_index_clr <= 1'b0;
			
			completed_ld <= 1'b0;
			completed_clr <= 1'b0;
			index_ld <= 1'b1;
			max_ld <= 1'b0;
			max_index_ld <= 1'b0;
		end
		Finish: begin
				nextState <= Reset;
			
			max_clr <= 1'b0;
			index_clr <= 1'b0;
			max_index_clr <= 1'b0;
			
			completed_ld <= 1'b1;
			completed_clr <= 1'b0;
			index_ld <= 1'b0;
			max_ld <= 1'b0;
			max_index_ld <= 1'b0;
		end
	endcase
end

always@(posedge clk) begin
	if(reset) begin
		state <= Reset;
	end
	else begin
		state <= nextState;
	end
end

endmodule
	
module RTL_Datapath(max_index, completed, clk, reset, input_array, update_max, index_lt_eight, index_ld, index_clr, max_ld, max_clr, max_index_ld, max_index_clr, completed_ld, completed_clr);

output reg [3:0] max_index;
output reg completed;

input wire clk;
input wire reset;
input wire [63:0] input_array;

wire signed [7:0] memoryData[0:7];
assign {memoryData[0],memoryData[1],memoryData[2],memoryData[3], memoryData[4],memoryData[5],memoryData[6],memoryData[7]} = input_array;

output reg update_max, index_lt_eight;

input index_ld, index_clr, max_ld, max_clr, max_index_ld, max_index_clr, completed_ld, completed_clr;

reg [3:0] index;
reg signed [7:0] max;

always@(negedge clk) begin
	if(completed_clr) begin
		completed <= 1'b0;
	end
	if(completed_ld) begin
		completed <= 1'b1;
	end
	
	if(memoryData[index] > max) begin
		update_max <= 1'b1;
	end
	else begin
		update_max <= 1'b0;
	end
	
	if(index_clr) begin
		index = 4'b0000;
	end
	if(index_ld) begin
		index = index + 1'b1;
	end
	
	if(max_clr) begin
		max <=  8'b10000000;
	end
	if(max_ld) begin
		max <= memoryData[index];
	end
	
	if(index >= 8) begin
		index_lt_eight <= 1'b0;
	end
	else begin
		index_lt_eight <= 1'b1;
	end
	
	if(max_index_clr) begin
		max_index <= 4'b0000;
	end
	if(max_index_ld) begin
		max_index <= index;
	end
end

endmodule
	