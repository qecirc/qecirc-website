OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[5];
z q[4];
z q[3];
z q[9];
id q[0];
swap q[6], q[9];
swap q[10], q[6];
swap q[4], q[9];
swap q[3], q[10];
swap q[5], q[6];
swap q[7], q[10];
