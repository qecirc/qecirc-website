OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[11];
z q[9];
z q[10];
z q[1];
z q[3];
z q[7];
swap q[14], q[12];
id q[0];
swap q[7], q[5];
swap q[10], q[14];
swap q[8], q[12];
swap q[3], q[7];
swap q[1], q[5];
swap q[13], q[10];
swap q[9], q[14];
swap q[6], q[3];
swap q[2], q[7];
swap q[11], q[10];
swap q[4], q[3];
