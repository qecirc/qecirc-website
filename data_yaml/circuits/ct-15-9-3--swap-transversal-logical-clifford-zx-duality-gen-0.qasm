OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

swap q[3], q[12];
swap q[11], q[5];
swap q[14], q[9];
swap q[0], q[6];
swap q[2], q[10];
swap q[4], q[13];
