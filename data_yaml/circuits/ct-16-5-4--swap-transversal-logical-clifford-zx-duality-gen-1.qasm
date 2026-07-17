OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

swap q[4], q[12];
swap q[6], q[13];
swap q[8], q[14];
swap q[10], q[2];
id q[0];
