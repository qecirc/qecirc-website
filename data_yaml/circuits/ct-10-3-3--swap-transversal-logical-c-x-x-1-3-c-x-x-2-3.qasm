OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[6];
z q[3];
z q[2];
z q[7];
swap q[9], q[8];
swap q[4], q[5];
id q[0];
swap q[3], q[2];
swap q[6], q[7];
