OPENQASM 2.0;
include "qelib1.inc";

qreg q[26];

swap q[6], q[14];
swap q[3], q[25];
swap q[19], q[11];
swap q[22], q[1];
swap q[15], q[7];
swap q[20], q[9];
id q[5];
