OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

swap q[12], q[11];
swap q[6], q[21];
swap q[4], q[25];
swap q[27], q[1];
swap q[15], q[8];
swap q[13], q[9];
id q[5];
