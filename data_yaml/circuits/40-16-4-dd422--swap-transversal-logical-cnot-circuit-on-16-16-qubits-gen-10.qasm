OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

swap q[20], q[8];
swap q[10], q[38];
swap q[9], q[29];
swap q[39], q[19];
id q[11];
