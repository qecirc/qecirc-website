OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[7];
z q[5];
z q[3];
z q[9];
swap q[10], q[6];
swap q[4], q[8];
id q[0];
swap q[5], q[9];
swap q[7], q[3];
