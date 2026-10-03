OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[9];
z q[4];
z q[15];
z q[10];
id q[0];
swap q[10], q[7];
swap q[5], q[15];
swap q[4], q[14];
swap q[9], q[6];
