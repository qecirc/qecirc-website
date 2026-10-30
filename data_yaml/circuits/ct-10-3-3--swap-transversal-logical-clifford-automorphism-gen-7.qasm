OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[3];
z q[2];
z q[8];
z q[7];
id q[0];
swap q[8], q[7];
swap q[5], q[7];
swap q[2], q[8];
swap q[9], q[7];
swap q[3], q[2];
swap q[6], q[9];
