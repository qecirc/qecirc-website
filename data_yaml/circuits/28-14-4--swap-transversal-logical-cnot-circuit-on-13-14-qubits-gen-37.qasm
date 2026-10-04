OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[6], q[8];
swap q[3], q[5];
swap q[19], q[17];
swap q[22], q[26];
swap q[16], q[20];
swap q[21], q[15];
