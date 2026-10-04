OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

swap q[10], q[7];
swap q[11], q[8];
swap q[5], q[15];
swap q[2], q[12];
id q[0];
