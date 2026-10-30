OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

swap q[8], q[3];
swap q[7], q[2];
swap q[6], q[1];
swap q[5], q[0];
swap q[9], q[4];
swap q[32], q[31];
swap q[28], q[27];
swap q[25], q[24];
swap q[22], q[21];
swap q[39], q[38];
id q[18];
