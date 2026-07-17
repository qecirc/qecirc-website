OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[10];
z q[5];
z q[4];
z q[3];
z q[16];
z q[11];
swap q[15], q[6];
id q[0];
swap q[5], q[16];
swap q[7], q[11];
swap q[10], q[8];
