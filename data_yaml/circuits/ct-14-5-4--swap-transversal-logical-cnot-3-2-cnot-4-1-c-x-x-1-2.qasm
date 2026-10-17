OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[8];
z q[2];
z q[1];
z q[0];
z q[3];
z q[9];
swap q[13], q[12];
swap q[4], q[5];
id q[7];
swap q[1], q[0];
swap q[2], q[3];
