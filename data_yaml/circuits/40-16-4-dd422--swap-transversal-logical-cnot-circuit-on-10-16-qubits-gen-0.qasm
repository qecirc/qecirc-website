OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

swap q[1], q[0];
swap q[31], q[30];
swap q[22], q[21];
swap q[12], q[11];
