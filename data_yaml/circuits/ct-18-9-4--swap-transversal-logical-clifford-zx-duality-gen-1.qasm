OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

z q[12];
z q[8];
z q[4];
z q[10];
z q[11];
z q[15];
swap q[16], q[9];
swap q[1], q[14];
swap q[3], q[7];
id q[0];
swap q[2], q[10];
swap q[4], q[17];
swap q[5], q[11];
swap q[6], q[15];
swap q[12], q[8];
