OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[12], q[2];
swap q[6], q[22];
swap q[4], q[18];
swap q[1], q[14];
swap q[0], q[13];
swap q[26], q[8];
id q[5];
