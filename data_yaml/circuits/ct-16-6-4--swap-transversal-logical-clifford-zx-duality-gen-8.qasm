OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[6];
z q[4];
z q[5];
z q[15];
z q[11];
z q[10];
swap q[12], q[7];
id q[0];
swap q[2], q[10];
swap q[13], q[15];
swap q[3], q[5];
swap q[14], q[12];
swap q[4], q[2];
swap q[6], q[15];
swap q[9], q[5];
