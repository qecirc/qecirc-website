OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[6];
z q[4];
z q[3];
z q[5];
z q[8];
z q[7];
id q[0];
swap q[8], q[10];
swap q[11], q[7];
swap q[15], q[10];
swap q[5], q[7];
swap q[12], q[11];
swap q[2], q[8];
swap q[13], q[12];
swap q[3], q[2];
swap q[6], q[7];
swap q[9], q[10];
swap q[14], q[2];
swap q[4], q[12];
