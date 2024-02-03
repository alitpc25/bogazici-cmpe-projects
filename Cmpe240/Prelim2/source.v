`timescale 1ns / 1ns
module source(i2, i1, i0, o);

wire i0i1, i0i2;
wire noti0;
input i2, i1, i0;
output o;

not(noti0,i0);
and(i0i1, i1, noti0);
and(i0i2, i0, i2);
or(o, i0i1, i0i2);


endmodule
