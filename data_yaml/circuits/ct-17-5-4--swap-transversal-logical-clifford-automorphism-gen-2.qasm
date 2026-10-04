OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

swap q[5], q[13];
swap q[7], q[14];
swap q[9], q[15];
swap q[11], q[3];
id q[0];
