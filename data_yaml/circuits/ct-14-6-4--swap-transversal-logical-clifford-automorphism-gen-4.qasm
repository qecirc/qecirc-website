OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[6], q[5];
swap q[9], q[8];
swap q[10], q[13];
swap q[0], q[3];
