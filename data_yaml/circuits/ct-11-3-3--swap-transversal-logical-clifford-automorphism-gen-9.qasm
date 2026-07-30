OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[5];
z q[3];
swap q[9], q[8];
id q[0];
swap q[6], q[9];
swap q[3], q[8];
swap q[4], q[3];
swap q[7], q[8];
swap q[5], q[3];
