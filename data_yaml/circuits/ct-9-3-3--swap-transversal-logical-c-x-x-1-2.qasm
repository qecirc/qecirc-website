OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

z q[5];
z q[3];
z q[1];
z q[7];
swap q[8], q[4];
swap q[2], q[6];
id q[0];
swap q[3], q[7];
swap q[5], q[1];
