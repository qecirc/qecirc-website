OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[8];
z q[6];
z q[4];
z q[11];
swap q[1], q[7];
swap q[2], q[9];
id q[0];
swap q[4], q[11];
swap q[8], q[6];
