OPENQASM 2.0;
include "qelib1.inc";

qreg q[27];

swap q[4], q[8];
swap q[3], q[7];
swap q[23], q[17];
swap q[18], q[26];
swap q[16], q[24];
swap q[25], q[15];
id q[5];
