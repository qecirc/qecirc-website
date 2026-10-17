OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[12], q[3];
swap q[6], q[23];
swap q[4], q[19];
swap q[1], q[16];
swap q[0], q[15];
swap q[26], q[9];
id q[5];
