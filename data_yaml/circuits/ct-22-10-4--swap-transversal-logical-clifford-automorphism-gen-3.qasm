OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

swap q[11], q[16];
swap q[21], q[20];
swap q[7], q[19];
swap q[3], q[15];
swap q[4], q[13];
swap q[5], q[10];
swap q[6], q[18];
swap q[12], q[8];
swap q[17], q[14];
id q[0];
