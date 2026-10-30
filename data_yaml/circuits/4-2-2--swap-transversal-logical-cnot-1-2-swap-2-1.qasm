OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];

swap q[2], q[3];
swap q[0], q[2];
