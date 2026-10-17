OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[6];
z q[3];
z q[2];
z q[10];
swap q[5], q[15];
swap q[13], q[11];
swap q[14], q[7];
id q[0];
swap q[3], q[8];
swap q[4], q[10];
swap q[9], q[6];
