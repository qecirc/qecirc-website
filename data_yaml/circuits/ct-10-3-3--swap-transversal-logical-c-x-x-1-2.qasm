OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[6];
z q[4];
z q[2];
z q[8];
swap q[9], q[5];
swap q[3], q[7];
id q[0];
swap q[4], q[8];
swap q[6], q[2];
