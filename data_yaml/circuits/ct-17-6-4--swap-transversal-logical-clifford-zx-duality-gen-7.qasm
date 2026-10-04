OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[5];
z q[4];
z q[12];
z q[11];
id q[0];
swap q[9], q[11];
swap q[12], q[8];
swap q[15], q[4];
swap q[5], q[14];
