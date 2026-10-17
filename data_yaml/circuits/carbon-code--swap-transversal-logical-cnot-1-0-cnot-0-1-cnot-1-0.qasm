OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

swap q[0], q[4];
swap q[1], q[11];
swap q[6], q[10];
swap q[7], q[5];
swap q[2], q[8];
