OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[0], q[26];
swap q[15], q[9];
swap q[13], q[8];
swap q[10], q[17];
swap q[20], q[7];
swap q[24], q[5];
