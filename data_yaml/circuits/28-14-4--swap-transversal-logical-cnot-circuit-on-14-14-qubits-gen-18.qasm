OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[6], q[25];
swap q[4], q[21];
swap q[3], q[14];
swap q[2], q[16];
swap q[0], q[17];
swap q[10], q[26];
id q[5];
