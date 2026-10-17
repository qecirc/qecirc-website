OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

z q[7];
z q[4];
z q[2];
z q[6];
id q[0];
swap q[6], q[1];
swap q[2], q[5];
swap q[4], q[8];
swap q[7], q[3];
