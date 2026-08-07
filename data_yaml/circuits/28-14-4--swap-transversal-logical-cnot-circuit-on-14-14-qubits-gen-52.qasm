OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[12], q[21];
swap q[6], q[11];
swap q[19], q[14];
swap q[18], q[16];
swap q[0], q[5];
swap q[24], q[26];
