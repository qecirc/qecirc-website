OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];

s q[3];
s q[2];
s q[1];
s q[0];
s q[4];
swap q[0], q[4];
swap q[1], q[0];
swap q[2], q[0];
