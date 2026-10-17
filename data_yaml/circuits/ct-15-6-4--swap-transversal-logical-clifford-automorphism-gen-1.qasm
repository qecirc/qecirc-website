OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[3];
z q[2];
z q[1];
z q[14];
z q[10];
swap q[12], q[4];
id q[0];
swap q[2], q[14];
swap q[5], q[10];
swap q[8], q[7];
