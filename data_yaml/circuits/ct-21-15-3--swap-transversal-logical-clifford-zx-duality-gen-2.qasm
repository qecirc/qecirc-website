OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

swap q[14], q[6];
swap q[17], q[3];
swap q[8], q[19];
swap q[0], q[11];
swap q[20], q[12];
swap q[1], q[9];
swap q[13], q[16];
swap q[5], q[2];
id q[7];
