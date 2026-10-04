OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[2], q[10];
swap q[22], q[20];
swap q[18], q[24];
swap q[27], q[13];
swap q[1], q[9];
swap q[16], q[26];
id q[5];
