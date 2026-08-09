OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[8], q[5];
swap q[9], q[6];
swap q[3], q[13];
swap q[0], q[10];
