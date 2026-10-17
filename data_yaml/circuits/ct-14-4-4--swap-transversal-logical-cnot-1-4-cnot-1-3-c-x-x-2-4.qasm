OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[6];
z q[13];
z q[5];
z q[12];
z q[3];
z q[10];
swap q[2], q[8];
swap q[4], q[11];
id q[0];
swap q[5], q[12];
swap q[6], q[13];
