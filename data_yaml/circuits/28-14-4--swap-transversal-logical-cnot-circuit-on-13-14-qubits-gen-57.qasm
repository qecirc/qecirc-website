OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[12], q[10];
swap q[6], q[20];
swap q[4], q[24];
swap q[27], q[0];
swap q[16], q[8];
swap q[14], q[9];
id q[5];
