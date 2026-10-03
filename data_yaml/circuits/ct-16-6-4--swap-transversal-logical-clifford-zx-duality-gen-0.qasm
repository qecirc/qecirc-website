OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[6];
z q[4];
z q[15];
z q[7];
swap q[11], q[8];
swap q[2], q[12];
id q[0];
swap q[4], q[14];
swap q[9], q[6];
