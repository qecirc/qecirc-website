OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[5], q[8];
swap q[1], q[12];
swap q[13], q[9];
swap q[2], q[6];
id q[0];
