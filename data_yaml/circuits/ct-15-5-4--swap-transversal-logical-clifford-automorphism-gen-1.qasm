OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[3], q[11];
swap q[5], q[12];
swap q[7], q[13];
swap q[9], q[1];
id q[0];
