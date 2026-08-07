OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[4], q[0];
swap q[19], q[15];
swap q[18], q[13];
swap q[27], q[24];
swap q[11], q[7];
swap q[21], q[17];
id q[5];
