OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];

swap q[1], q[2];
id q[3];
