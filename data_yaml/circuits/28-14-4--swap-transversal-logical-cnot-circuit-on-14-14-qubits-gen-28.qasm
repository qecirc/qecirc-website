OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[6], q[24];
swap q[4], q[20];
swap q[3], q[13];
swap q[2], q[15];
swap q[1], q[17];
swap q[11], q[26];
id q[5];
