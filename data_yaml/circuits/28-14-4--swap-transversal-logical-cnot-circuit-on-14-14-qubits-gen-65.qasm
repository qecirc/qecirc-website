OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

swap q[12], q[5];
swap q[4], q[17];
swap q[23], q[8];
swap q[22], q[9];
swap q[1], q[20];
swap q[21], q[0];
