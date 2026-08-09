OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

swap q[12], q[6];
swap q[3], q[23];
swap q[2], q[22];
swap q[11], q[21];
swap q[10], q[20];
swap q[17], q[7];
id q[5];
