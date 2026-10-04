OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[1];
z q[14];
z q[10];
z q[7];
z q[6];
swap q[3], q[11];
id q[0];
swap q[13], q[1];
swap q[5], q[10];
swap q[8], q[7];
