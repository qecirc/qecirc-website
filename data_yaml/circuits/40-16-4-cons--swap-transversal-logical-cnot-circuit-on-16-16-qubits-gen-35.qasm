OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

swap q[12], q[10];
swap q[1], q[31];
swap q[0], q[30];
swap q[11], q[29];
id q[39];
