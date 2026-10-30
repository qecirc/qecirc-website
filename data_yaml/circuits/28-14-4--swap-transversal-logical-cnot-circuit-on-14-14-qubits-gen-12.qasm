OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[2], q[11];
swap q[22], q[21];
swap q[18], q[25];
swap q[27], q[14];
swap q[0], q[9];
swap q[15], q[26];
id q[5];
