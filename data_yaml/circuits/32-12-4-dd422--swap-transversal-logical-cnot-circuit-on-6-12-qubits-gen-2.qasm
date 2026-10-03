OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[3], q[2];
swap q[27], q[26];
swap q[20], q[19];
swap q[12], q[11];
id q[9];
