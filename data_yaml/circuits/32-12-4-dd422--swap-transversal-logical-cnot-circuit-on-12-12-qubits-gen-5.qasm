OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

swap q[16], q[8];
swap q[6], q[30];
swap q[5], q[29];
swap q[4], q[28];
swap q[3], q[27];
swap q[2], q[26];
swap q[1], q[25];
swap q[0], q[24];
id q[9];
