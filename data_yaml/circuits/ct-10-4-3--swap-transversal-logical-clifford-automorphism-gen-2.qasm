OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[2];
z q[1];
swap q[5], q[6];
swap q[0], q[3];
swap q[8], q[9];
swap q[2], q[1];
