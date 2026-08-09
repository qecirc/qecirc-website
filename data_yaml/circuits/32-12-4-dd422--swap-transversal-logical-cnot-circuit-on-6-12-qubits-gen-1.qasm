OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[2], q[1];
swap q[26], q[25];
swap q[19], q[18];
swap q[11], q[10];
id q[9];
