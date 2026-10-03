OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[4];
z q[11];
z q[3];
z q[10];
z q[1];
z q[8];
swap q[0], q[6];
swap q[2], q[9];
swap q[3], q[10];
swap q[4], q[11];
