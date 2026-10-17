OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

swap q[8], q[7];
swap q[30], q[23];
swap q[29], q[22];
swap q[28], q[21];
swap q[27], q[20];
swap q[26], q[19];
swap q[25], q[18];
swap q[24], q[17];
id q[9];
