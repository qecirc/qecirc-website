OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[12], q[8];
swap q[1], q[5];
swap q[6], q[13];
swap q[2], q[9];
id q[0];
