OPENQASM 2.0;
include "qelib1.inc";

qreg q[26];

swap q[6], q[16];
swap q[23], q[1];
swap q[2], q[25];
swap q[18], q[11];
swap q[13], q[7];
swap q[20], q[8];
id q[5];
