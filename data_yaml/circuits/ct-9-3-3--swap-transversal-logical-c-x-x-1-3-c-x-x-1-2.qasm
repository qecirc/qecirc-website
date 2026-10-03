OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

z q[1];
z q[4];
z q[7];
z q[6];
id q[0];
swap q[1], q[8];
swap q[2], q[7];
swap q[3], q[6];
swap q[5], q[4];
