OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[6], q[27];
swap q[3], q[18];
swap q[19], q[2];
swap q[1], q[21];
swap q[0], q[20];
swap q[26], q[7];
id q[5];
