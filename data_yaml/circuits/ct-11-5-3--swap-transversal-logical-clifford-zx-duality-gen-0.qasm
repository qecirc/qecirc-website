OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[0];
z q[10];
z q[8];
z q[5];
z q[9];
z q[3];
swap q[1], q[7];
swap q[5], q[3];
swap q[8], q[9];
swap q[0], q[10];
