OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[11];
z q[9];
z q[5];
z q[4];
z q[13];
z q[12];
swap q[3], q[15];
id q[0];
swap q[12], q[10];
swap q[4], q[16];
swap q[11], q[9];
