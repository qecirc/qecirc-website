OPENQASM 2.0;
include "qelib1.inc";

qreg q[26];

swap q[12], q[16];
swap q[3], q[1];
swap q[22], q[25];
swap q[18], q[21];
swap q[13], q[17];
swap q[10], q[8];
id q[5];
