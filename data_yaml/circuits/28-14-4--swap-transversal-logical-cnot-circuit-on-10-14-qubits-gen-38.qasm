OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

swap q[6], q[5];
swap q[4], q[7];
swap q[3], q[8];
swap q[2], q[9];
swap q[1], q[10];
swap q[11], q[0];
