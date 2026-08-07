OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[12], q[26];
swap q[3], q[9];
swap q[2], q[8];
swap q[27], q[17];
swap q[21], q[24];
swap q[25], q[20];
id q[5];
