OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[5], q[10];
swap q[13], q[2];
swap q[4], q[3];
swap q[12], q[11];
id q[8];
