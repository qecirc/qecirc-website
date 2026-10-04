OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[6], q[26];
swap q[23], q[9];
swap q[22], q[8];
swap q[27], q[7];
swap q[11], q[24];
swap q[25], q[10];
id q[5];
