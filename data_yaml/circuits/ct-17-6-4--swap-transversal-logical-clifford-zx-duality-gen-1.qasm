OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[10];
z q[5];
z q[16];
z q[11];
id q[0];
swap q[11], q[8];
swap q[6], q[16];
swap q[5], q[15];
swap q[10], q[7];
