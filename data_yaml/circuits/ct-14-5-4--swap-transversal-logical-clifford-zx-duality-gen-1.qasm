OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

swap q[2], q[10];
swap q[4], q[11];
swap q[6], q[12];
swap q[8], q[0];
id q[7];
