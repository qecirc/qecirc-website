OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

z q[6];
z q[3];
z q[1];
z q[5];
swap q[5], q[0];
swap q[1], q[4];
swap q[3], q[7];
swap q[6], q[2];
