OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

swap q[5], q[9];
swap q[8], q[3];
swap q[0], q[10];
swap q[4], q[2];
