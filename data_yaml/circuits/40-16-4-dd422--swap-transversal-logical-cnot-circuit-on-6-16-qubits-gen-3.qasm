OPENQASM 2.0;
include "qelib1.inc";

qreg q[35];

swap q[4], q[3];
swap q[34], q[33];
swap q[25], q[24];
swap q[15], q[14];
id q[11];
