OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

z q[7];
z q[2];
z q[6];
z q[3];
swap q[7], q[5];
swap q[4], q[6];
swap q[1], q[3];
swap q[0], q[2];
