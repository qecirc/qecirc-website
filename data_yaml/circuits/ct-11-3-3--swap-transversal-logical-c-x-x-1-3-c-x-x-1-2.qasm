OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[3];
z q[6];
z q[9];
z q[8];
id q[0];
swap q[3], q[10];
swap q[4], q[9];
swap q[5], q[8];
swap q[7], q[6];
