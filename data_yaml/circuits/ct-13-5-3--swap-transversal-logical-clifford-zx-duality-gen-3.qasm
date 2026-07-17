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
swap q[6], q[4];
id q[0];
swap q[11], q[5];
swap q[10], q[7];
