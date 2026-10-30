OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

swap q[8], q[5];
swap q[4], q[12];
swap q[2], q[7];
swap q[1], q[9];
swap q[0], q[13];
swap q[10], q[15];
