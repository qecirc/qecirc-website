OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

swap q[14], q[3];
swap q[17], q[6];
swap q[19], q[11];
swap q[0], q[8];
swap q[9], q[12];
swap q[1], q[20];
swap q[2], q[16];
swap q[5], q[13];
id q[7];
