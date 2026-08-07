OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[12], q[24];
swap q[4], q[10];
swap q[23], q[13];
swap q[22], q[15];
swap q[1], q[7];
swap q[21], q[26];
id q[5];
