OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[10];
z q[8];
z q[4];
z q[3];
z q[12];
z q[11];
swap q[2], q[14];
id q[0];
swap q[11], q[9];
swap q[3], q[15];
swap q[10], q[8];
