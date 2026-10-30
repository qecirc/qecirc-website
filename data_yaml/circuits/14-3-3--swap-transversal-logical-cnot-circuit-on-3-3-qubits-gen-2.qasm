OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[5], q[13];
swap q[4], q[1];
swap q[12], q[9];
swap q[2], q[0];
swap q[10], q[8];
