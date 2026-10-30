OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

swap q[15], q[19];
swap q[1], q[10];
swap q[6], q[12];
swap q[2], q[9];
swap q[3], q[17];
swap q[4], q[18];
swap q[5], q[14];
swap q[13], q[11];
swap q[16], q[8];
id q[0];
