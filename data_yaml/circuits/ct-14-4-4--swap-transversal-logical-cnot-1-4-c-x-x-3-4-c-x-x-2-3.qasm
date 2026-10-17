OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[9];
z q[7];
z q[6];
z q[13];
z q[3];
z q[10];
swap q[4], q[11];
id q[0];
swap q[3], q[10];
swap q[6], q[13];
swap q[9], q[7];
