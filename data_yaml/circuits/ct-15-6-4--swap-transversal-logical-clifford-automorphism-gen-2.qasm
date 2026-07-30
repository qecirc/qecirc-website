OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[3];
z q[2];
z q[10];
z q[9];
id q[0];
swap q[9], q[6];
swap q[10], q[7];
swap q[2], q[12];
swap q[3], q[13];
