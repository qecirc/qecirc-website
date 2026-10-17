OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

z q[2];
z q[4];
swap q[7], q[6];
id q[0];
swap q[4], q[7];
swap q[8], q[4];
swap q[2], q[7];
swap q[3], q[2];
swap q[5], q[2];
