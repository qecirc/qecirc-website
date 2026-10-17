OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[4];
z q[2];
z q[1];
z q[9];
z q[0];
z q[3];
z q[5];
id q[6];
swap q[0], q[3];
swap q[1], q[8];
swap q[2], q[9];
swap q[7], q[4];
