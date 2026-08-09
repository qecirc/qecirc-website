OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

swap q[6], q[9];
swap q[2], q[13];
swap q[14], q[10];
swap q[3], q[7];
id q[0];
