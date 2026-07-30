OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

z q[3];
z q[2];
z q[7];
z q[6];
id q[0];
swap q[4], q[7];
swap q[1], q[6];
swap q[3], q[8];
swap q[5], q[2];
