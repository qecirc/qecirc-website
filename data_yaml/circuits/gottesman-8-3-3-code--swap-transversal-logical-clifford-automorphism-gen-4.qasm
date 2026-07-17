OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

z q[4];
z q[3];
swap q[6], q[3];
swap q[2], q[3];
swap q[7], q[6];
swap q[5], q[2];
swap q[4], q[3];
swap q[1], q[3];
