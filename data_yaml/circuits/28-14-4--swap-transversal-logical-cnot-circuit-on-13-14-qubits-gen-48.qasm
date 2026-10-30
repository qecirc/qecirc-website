OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[12], q[1];
swap q[3], q[16];
swap q[2], q[14];
swap q[27], q[11];
swap q[20], q[5];
swap q[24], q[7];
