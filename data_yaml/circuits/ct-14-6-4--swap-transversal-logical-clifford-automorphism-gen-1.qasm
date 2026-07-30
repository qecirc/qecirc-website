OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[4];
z q[2];
z q[13];
z q[5];
swap q[9], q[6];
swap q[0], q[10];
swap q[2], q[12];
swap q[7], q[4];
