OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[12], q[20];
swap q[6], q[10];
swap q[19], q[13];
swap q[18], q[15];
swap q[1], q[5];
swap q[25], q[26];
