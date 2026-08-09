OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

swap q[12], q[1];
swap q[10], q[31];
swap q[9], q[28];
swap q[8], q[26];
swap q[7], q[24];
swap q[6], q[22];
swap q[5], q[20];
swap q[4], q[18];
swap q[3], q[16];
swap q[2], q[14];
id q[39];
