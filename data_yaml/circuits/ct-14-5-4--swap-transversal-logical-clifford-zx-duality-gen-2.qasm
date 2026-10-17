OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[4];
z q[1];
z q[3];
z q[11];
z q[10];
z q[9];
swap q[13], q[12];
id q[7];
swap q[3], q[10];
swap q[5], q[11];
swap q[1], q[0];
swap q[6], q[13];
swap q[2], q[10];
swap q[4], q[11];
swap q[8], q[1];
