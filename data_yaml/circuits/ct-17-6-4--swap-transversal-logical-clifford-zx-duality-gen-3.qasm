OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[7];
z q[5];
z q[16];
z q[8];
swap q[12], q[9];
swap q[3], q[13];
id q[0];
swap q[5], q[15];
swap q[10], q[7];
