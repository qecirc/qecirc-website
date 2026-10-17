OPENQASM 2.0;
include "qelib1.inc";

qreg q[37];

swap q[6], q[5];
swap q[36], q[35];
swap q[27], q[26];
swap q[17], q[16];
id q[11];
