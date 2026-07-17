OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[2];
z q[1];
z q[6];
z q[5];
swap q[3], q[13];
swap q[0], q[10];
swap q[1], q[11];
swap q[2], q[12];
