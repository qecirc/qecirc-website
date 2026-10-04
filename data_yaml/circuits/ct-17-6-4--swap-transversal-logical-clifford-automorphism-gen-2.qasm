OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[5];
z q[4];
z q[9];
z q[8];
swap q[6], q[16];
swap q[3], q[13];
id q[0];
swap q[4], q[14];
swap q[5], q[15];
