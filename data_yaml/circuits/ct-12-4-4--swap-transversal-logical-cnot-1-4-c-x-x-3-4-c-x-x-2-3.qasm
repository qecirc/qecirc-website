OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[7];
z q[5];
z q[4];
z q[11];
z q[1];
z q[8];
swap q[2], q[9];
id q[6];
swap q[1], q[8];
swap q[4], q[11];
swap q[7], q[5];
