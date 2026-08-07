OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

swap q[8], q[6];
swap q[4], q[10];
swap q[2], q[12];
swap q[1], q[7];
swap q[0], q[14];
swap q[9], q[15];
swap q[3], q[5];
swap q[13], q[11];
