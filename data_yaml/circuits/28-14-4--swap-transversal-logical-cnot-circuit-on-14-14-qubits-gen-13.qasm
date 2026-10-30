OPENQASM 2.0;
include "qelib1.inc";

qreg q[25];

swap q[4], q[16];
swap q[19], q[1];
swap q[2], q[21];
swap q[22], q[11];
swap q[13], q[5];
swap q[24], q[8];
