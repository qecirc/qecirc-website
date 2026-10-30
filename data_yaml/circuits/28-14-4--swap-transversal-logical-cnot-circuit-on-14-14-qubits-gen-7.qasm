OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[4], q[27];
swap q[3], q[22];
swap q[23], q[2];
swap q[1], q[25];
swap q[0], q[24];
swap q[26], q[5];
