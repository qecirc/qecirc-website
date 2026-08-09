OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

swap q[13], q[7];
swap q[12], q[6];
swap q[11], q[5];
swap q[10], q[9];
swap q[14], q[8];
swap q[32], q[33];
swap q[27], q[28];
swap q[21], q[24];
swap q[18], q[17];
swap q[39], q[36];
id q[38];
