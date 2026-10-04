OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[7];
z q[4];
z q[6];
z q[9];
id q[0];
swap q[6], q[8];
swap q[3], q[9];
swap q[4], q[10];
swap q[7], q[5];
