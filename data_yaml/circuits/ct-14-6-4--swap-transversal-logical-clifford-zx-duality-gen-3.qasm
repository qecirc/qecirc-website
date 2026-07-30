OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[10], q[13];
swap q[0], q[3];
swap q[12], q[11];
swap q[2], q[1];
id q[5];
