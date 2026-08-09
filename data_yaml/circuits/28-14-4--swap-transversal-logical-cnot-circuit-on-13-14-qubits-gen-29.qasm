OPENQASM 2.0;
include "qelib1.inc";

qreg q[26];

swap q[1], q[0];
swap q[16], q[15];
swap q[14], q[13];
swap q[11], q[10];
swap q[21], q[20];
swap q[25], q[24];
id q[5];
