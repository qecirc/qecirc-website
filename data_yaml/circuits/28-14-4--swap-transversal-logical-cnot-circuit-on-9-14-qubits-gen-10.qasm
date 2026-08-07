OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[4], q[1];
swap q[19], q[16];
swap q[18], q[14];
swap q[27], q[25];
swap q[10], q[7];
swap q[20], q[17];
id q[5];
