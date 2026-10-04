OPENQASM 2.0;
include "qelib1.inc";

qreg q[25];

swap q[6], q[13];
swap q[3], q[24];
swap q[19], q[10];
swap q[22], q[0];
swap q[16], q[7];
swap q[21], q[9];
id q[5];
