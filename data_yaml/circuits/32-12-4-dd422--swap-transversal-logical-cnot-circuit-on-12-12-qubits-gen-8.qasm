OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

swap q[16], q[6];
swap q[8], q[30];
swap q[7], q[23];
swap q[31], q[15];
id q[9];
