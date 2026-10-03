OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

z q[8];
z q[6];
z q[5];
z q[12];
z q[2];
z q[9];
swap q[3], q[10];
id q[0];
swap q[2], q[9];
swap q[5], q[12];
swap q[8], q[6];
