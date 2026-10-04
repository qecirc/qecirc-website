OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[2];
z q[14];
z q[10];
id q[0];
swap q[10], q[7];
swap q[4], q[14];
swap q[2], q[12];
swap q[8], q[5];
