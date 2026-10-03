OPENQASM 2.0;
include "qelib1.inc";

qreg q[33];

swap q[2], q[1];
swap q[32], q[31];
swap q[23], q[22];
swap q[13], q[12];
id q[11];
