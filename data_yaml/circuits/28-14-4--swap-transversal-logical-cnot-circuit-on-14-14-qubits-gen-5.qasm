OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[6], q[18];
swap q[4], q[22];
swap q[3], q[27];
swap q[16], q[11];
swap q[15], q[10];
swap q[9], q[17];
id q[5];
