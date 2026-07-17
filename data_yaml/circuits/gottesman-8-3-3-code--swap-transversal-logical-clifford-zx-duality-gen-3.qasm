OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

z q[4];
z q[7];
z q[2];
z q[6];
swap q[6], q[3];
swap q[2], q[6];
swap q[5], q[3];
swap q[7], q[3];
swap q[1], q[6];
swap q[0], q[5];
