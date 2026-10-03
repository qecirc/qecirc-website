OPENQASM 2.0;
include "qelib1.inc";

qreg q[34];

swap q[3], q[2];
swap q[33], q[32];
swap q[24], q[23];
swap q[14], q[13];
id q[11];
