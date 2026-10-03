OPENQASM 2.0;
include "qelib1.inc";

qreg q[26];

swap q[12], q[14];
swap q[23], q[25];
swap q[19], q[21];
swap q[2], q[1];
swap q[15], q[17];
swap q[10], q[9];
id q[5];
