OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[6];
z q[3];
z q[5];
z q[8];
id q[0];
swap q[5], q[7];
swap q[2], q[8];
swap q[3], q[9];
swap q[6], q[4];
