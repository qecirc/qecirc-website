OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];

swap q[0], q[1];
id q[3];
