OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[7];
z q[3];
z q[2];
z q[1];
z q[4];
z q[10];
z q[6];
z q[8];
swap q[5], q[9];
swap q[0], q[11];
swap q[2], q[1];
swap q[7], q[3];
