OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[8];
z q[6];
z q[2];
z q[1];
z q[10];
z q[9];
swap q[0], q[12];
swap q[9], q[7];
swap q[1], q[13];
swap q[8], q[6];
