OPENQASM 2.0;
include "qelib1.inc";

qreg q[30];

swap q[5], q[4];
swap q[29], q[28];
swap q[22], q[21];
swap q[14], q[13];
id q[9];
