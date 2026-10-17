OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[9];
z q[7];
z q[5];
z q[4];
z q[2];
z q[14];
z q[10];
z q[15];
swap q[12], q[8];
swap q[3], q[16];
id q[0];
swap q[1], q[10];
swap q[2], q[14];
swap q[4], q[13];
swap q[5], q[8];
swap q[9], q[16];
swap q[6], q[10];
swap q[7], q[14];
swap q[11], q[13];
