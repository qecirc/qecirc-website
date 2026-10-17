OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[7];
z q[5];
z q[3];
z q[10];
swap q[0], q[6];
swap q[1], q[8];
swap q[3], q[10];
swap q[7], q[5];
