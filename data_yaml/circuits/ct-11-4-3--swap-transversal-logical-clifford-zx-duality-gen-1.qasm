OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[5];
z q[3];
z q[2];
z q[10];
z q[1];
z q[4];
z q[6];
id q[0];
swap q[1], q[4];
swap q[2], q[9];
swap q[3], q[10];
swap q[8], q[5];
