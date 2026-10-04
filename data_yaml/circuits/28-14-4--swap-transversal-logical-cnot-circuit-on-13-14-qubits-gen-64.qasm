OPENQASM 2.0;
include "qelib1.inc";

qreg q[26];

swap q[12], q[7];
swap q[6], q[17];
swap q[19], q[8];
swap q[18], q[9];
swap q[1], q[24];
swap q[25], q[0];
id q[5];
