OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[10];
z q[8];
z q[7];
z q[14];
z q[4];
z q[11];
swap q[5], q[12];
id q[0];
swap q[4], q[11];
swap q[7], q[14];
swap q[10], q[8];
