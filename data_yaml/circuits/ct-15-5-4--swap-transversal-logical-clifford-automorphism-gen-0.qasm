OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[9];
z q[7];
z q[3];
z q[2];
z q[11];
z q[10];
swap q[1], q[13];
id q[0];
swap q[10], q[8];
swap q[2], q[14];
swap q[9], q[7];
