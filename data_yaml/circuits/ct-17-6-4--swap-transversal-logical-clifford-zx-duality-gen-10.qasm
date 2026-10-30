OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[10];
z q[3];
z q[6];
z q[8];
swap q[9], q[11];
id q[0];
swap q[12], q[8];
swap q[6], q[11];
swap q[5], q[9];
swap q[16], q[8];
swap q[13], q[6];
swap q[15], q[12];
swap q[3], q[16];
swap q[14], q[13];
swap q[4], q[3];
swap q[10], q[14];
swap q[7], q[4];
