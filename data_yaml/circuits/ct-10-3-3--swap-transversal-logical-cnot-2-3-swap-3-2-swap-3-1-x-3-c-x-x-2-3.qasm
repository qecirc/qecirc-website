OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[6];
z q[4];
z q[3];
z q[2];
z q[5];
z q[8];
id q[0];
swap q[8], q[7];
swap q[9], q[7];
swap q[2], q[9];
swap q[4], q[7];
swap q[3], q[9];
swap q[6], q[2];
