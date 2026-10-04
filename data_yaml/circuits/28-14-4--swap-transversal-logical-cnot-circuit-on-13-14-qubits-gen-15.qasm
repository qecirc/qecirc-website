OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[3], q[11];
swap q[23], q[21];
swap q[19], q[25];
swap q[27], q[16];
swap q[0], q[8];
swap q[13], q[26];
id q[5];
