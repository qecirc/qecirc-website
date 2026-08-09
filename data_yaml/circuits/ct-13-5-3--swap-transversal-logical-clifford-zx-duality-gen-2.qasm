OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

z q[2];
z q[12];
z q[10];
z q[7];
z q[11];
z q[5];
swap q[3], q[9];
id q[0];
swap q[7], q[5];
swap q[10], q[11];
swap q[2], q[12];
