OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[12], q[27];
swap q[23], q[18];
swap q[19], q[22];
swap q[1], q[11];
swap q[0], q[10];
swap q[26], q[17];
id q[5];
