OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[6], q[19];
swap q[4], q[23];
swap q[2], q[27];
swap q[14], q[11];
swap q[13], q[10];
swap q[8], q[17];
id q[5];
