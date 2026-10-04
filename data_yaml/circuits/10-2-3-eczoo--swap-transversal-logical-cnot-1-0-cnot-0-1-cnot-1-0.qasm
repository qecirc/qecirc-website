OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

swap q[5], q[2];
swap q[1], q[0];
swap q[8], q[9];
swap q[7], q[4];
swap q[6], q[3];
