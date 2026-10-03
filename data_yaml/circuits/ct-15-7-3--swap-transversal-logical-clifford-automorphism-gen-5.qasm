OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[3];
z q[7];
z q[14];
z q[10];
z q[6];
z q[13];
swap q[4], q[12];
swap q[5], q[11];
id q[0];
swap q[13], q[9];
swap q[2], q[6];
