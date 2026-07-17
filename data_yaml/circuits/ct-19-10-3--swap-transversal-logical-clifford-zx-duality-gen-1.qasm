OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

swap q[17], q[6];
swap q[12], q[9];
swap q[3], q[15];
swap q[18], q[7];
swap q[13], q[10];
swap q[4], q[16];
id q[0];
