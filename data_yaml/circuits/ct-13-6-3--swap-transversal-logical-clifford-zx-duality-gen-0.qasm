OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

z q[8];
z q[4];
z q[3];
z q[2];
z q[5];
z q[11];
z q[7];
z q[9];
swap q[6], q[10];
swap q[1], q[12];
id q[0];
swap q[3], q[2];
swap q[8], q[4];
