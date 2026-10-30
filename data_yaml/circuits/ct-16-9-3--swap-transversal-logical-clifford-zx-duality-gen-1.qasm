OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[3];
z q[14];
swap q[4], q[13];
swap q[7], q[10];
swap q[1], q[15];
swap q[2], q[8];
swap q[5], q[11];
id q[0];
swap q[3], q[14];
