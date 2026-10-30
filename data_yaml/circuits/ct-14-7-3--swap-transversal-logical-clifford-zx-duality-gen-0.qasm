OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[13], q[9];
swap q[2], q[6];
swap q[3], q[10];
swap q[4], q[11];
id q[0];
