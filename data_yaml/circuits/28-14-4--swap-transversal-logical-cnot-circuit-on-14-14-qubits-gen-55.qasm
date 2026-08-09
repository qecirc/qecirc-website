OPENQASM 2.0;
include "qelib1.inc";

qreg q[25];

swap q[12], q[15];
swap q[3], q[0];
swap q[22], q[24];
swap q[18], q[20];
swap q[14], q[17];
swap q[11], q[8];
id q[5];
