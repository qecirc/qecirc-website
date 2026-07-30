OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[5], q[12];
swap q[1], q[8];
swap q[6], q[9];
swap q[2], q[13];
id q[0];
