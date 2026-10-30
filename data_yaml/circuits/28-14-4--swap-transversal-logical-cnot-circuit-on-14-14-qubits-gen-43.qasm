OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[12], q[19];
swap q[4], q[3];
swap q[22], q[27];
swap q[14], q[21];
swap q[13], q[20];
swap q[8], q[7];
id q[5];
