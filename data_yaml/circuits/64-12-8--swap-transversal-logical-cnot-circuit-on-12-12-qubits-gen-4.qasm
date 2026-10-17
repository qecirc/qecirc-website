OPENQASM 2.0;
include "qelib1.inc";

qreg q[64];

swap q[48], q[7];
swap q[40], q[56];
swap q[39], q[49];
swap q[63], q[41];
swap q[31], q[9];
swap q[27], q[35];
swap q[26], q[32];
swap q[38], q[28];
swap q[10], q[3];
swap q[36], q[37];
swap q[33], q[34];
swap q[29], q[30];
swap q[8], q[2];
swap q[57], q[58];
swap q[50], q[51];
swap q[42], q[43];
id q[46];
