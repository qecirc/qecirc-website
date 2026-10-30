OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[7];
z q[6];
z q[3];
z q[10];
z q[8];
z q[15];
swap q[12], q[14];
id q[0];
swap q[16], q[8];
swap q[13], q[10];
swap q[3], q[12];
swap q[1], q[16];
swap q[2], q[13];
swap q[6], q[3];
swap q[4], q[1];
swap q[5], q[2];
swap q[11], q[6];
swap q[7], q[4];
swap q[9], q[5];
