OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[12], q[25];
swap q[4], q[11];
swap q[23], q[14];
swap q[22], q[16];
swap q[0], q[7];
swap q[20], q[26];
id q[5];
