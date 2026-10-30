OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[1];
z q[11];
z q[9];
z q[6];
z q[10];
z q[4];
swap q[2], q[8];
swap q[5], q[3];
id q[0];
swap q[10], q[4];
swap q[9], q[6];
