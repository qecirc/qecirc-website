OPENQASM 2.0;
include "qelib1.inc";

qreg q[25];

swap q[6], q[15];
swap q[23], q[0];
swap q[2], q[24];
swap q[18], q[10];
swap q[14], q[7];
swap q[21], q[8];
id q[5];
