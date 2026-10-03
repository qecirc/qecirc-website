OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

swap q[4], q[7];
swap q[0], q[11];
swap q[12], q[8];
swap q[1], q[5];
