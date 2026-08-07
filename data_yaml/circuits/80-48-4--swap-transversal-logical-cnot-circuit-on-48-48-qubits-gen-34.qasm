OPENQASM 2.0;
include "qelib1.inc";

qreg q[80];

swap q[16], q[5];
swap q[14], q[71];
swap q[13], q[64];
swap q[12], q[58];
swap q[11], q[52];
swap q[10], q[46];
swap q[9], q[40];
swap q[8], q[34];
swap q[7], q[28];
swap q[6], q[22];
id q[79];
