OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[12], q[18];
swap q[4], q[2];
swap q[23], q[27];
swap q[16], q[21];
swap q[15], q[20];
swap q[9], q[7];
id q[5];
