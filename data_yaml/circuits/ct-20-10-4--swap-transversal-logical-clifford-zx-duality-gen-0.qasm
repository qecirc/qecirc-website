OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

swap q[9], q[18];
swap q[0], q[19];
swap q[5], q[13];
swap q[1], q[11];
swap q[2], q[8];
swap q[3], q[16];
swap q[4], q[17];
swap q[7], q[6];
swap q[15], q[10];
