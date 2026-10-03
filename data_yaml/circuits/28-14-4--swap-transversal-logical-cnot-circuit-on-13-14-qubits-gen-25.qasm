OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[3], q[10];
swap q[23], q[20];
swap q[19], q[24];
swap q[27], q[15];
swap q[1], q[8];
swap q[14], q[26];
id q[5];
