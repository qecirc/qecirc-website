OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

swap q[18], q[12];
swap q[10], q[14];
swap q[2], q[16];
swap q[6], q[3];
swap q[7], q[4];
swap q[8], q[5];
swap q[13], q[19];
swap q[15], q[9];
swap q[17], q[11];
id q[0];
