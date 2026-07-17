OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

swap q[13], q[9];
swap q[2], q[6];
swap q[7], q[14];
swap q[3], q[10];
id q[0];
