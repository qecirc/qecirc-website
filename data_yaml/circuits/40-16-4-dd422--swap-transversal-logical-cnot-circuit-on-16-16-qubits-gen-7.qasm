OPENQASM 2.0;
include "qelib1.inc";

qreg q[39];

swap q[20], q[10];
swap q[8], q[38];
swap q[7], q[37];
swap q[6], q[36];
swap q[5], q[35];
swap q[4], q[34];
swap q[3], q[33];
swap q[2], q[32];
swap q[1], q[31];
swap q[0], q[30];
id q[11];
