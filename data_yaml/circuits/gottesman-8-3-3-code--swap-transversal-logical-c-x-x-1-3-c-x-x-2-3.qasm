OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

z q[0];
z q[1];
z q[2];
z q[3];
swap q[6], q[3];
swap q[7], q[2];
swap q[1], q[4];
swap q[0], q[5];
