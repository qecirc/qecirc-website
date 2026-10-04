OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

swap q[11], q[7];
swap q[0], q[4];
swap q[5], q[12];
swap q[1], q[8];
