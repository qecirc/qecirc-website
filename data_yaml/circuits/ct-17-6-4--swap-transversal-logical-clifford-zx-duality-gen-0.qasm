OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

swap q[14], q[8];
swap q[4], q[11];
swap q[15], q[9];
swap q[5], q[12];
id q[0];
