OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

swap q[13], q[8];
swap q[3], q[11];
swap q[14], q[7];
swap q[4], q[10];
id q[0];
