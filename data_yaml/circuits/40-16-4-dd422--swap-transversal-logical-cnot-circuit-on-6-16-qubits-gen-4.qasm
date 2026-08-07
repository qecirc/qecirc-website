OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

swap q[5], q[4];
swap q[35], q[34];
swap q[26], q[25];
swap q[16], q[15];
id q[11];
