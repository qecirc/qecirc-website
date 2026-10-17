OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[5];
z q[2];
z q[4];
z q[14];
z q[9];
swap q[12], q[6];
id q[0];
swap q[2], q[9];
swap q[5], q[11];
swap q[8], q[1];
