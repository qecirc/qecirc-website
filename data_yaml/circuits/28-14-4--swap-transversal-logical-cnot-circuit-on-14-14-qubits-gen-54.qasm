OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[12], q[0];
swap q[3], q[15];
swap q[2], q[13];
swap q[27], q[10];
swap q[21], q[5];
swap q[25], q[7];
