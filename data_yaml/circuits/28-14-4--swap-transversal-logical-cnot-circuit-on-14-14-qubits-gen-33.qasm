OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[4], q[9];
swap q[19], q[26];
swap q[2], q[7];
swap q[22], q[17];
swap q[14], q[24];
swap q[25], q[13];
id q[5];
