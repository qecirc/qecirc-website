OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

swap q[11], q[7];
swap q[0], q[4];
swap q[12], q[8];
swap q[1], q[5];
swap q[9], q[10];
swap q[3], q[2];
