OPENQASM 2.0;
include "qelib1.inc";

qreg q[26];

swap q[12], q[4];
swap q[3], q[19];
swap q[2], q[18];
swap q[11], q[25];
swap q[10], q[24];
swap q[17], q[5];
