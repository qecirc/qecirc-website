OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

swap q[24], q[10];
swap q[18], q[11];
swap q[17], q[13];
swap q[35], q[16];
swap q[9], q[32];
swap q[7], q[26];
swap q[6], q[34];
swap q[5], q[3];
swap q[8], q[20];
swap q[4], q[21];
swap q[2], q[22];
swap q[14], q[28];
swap q[12], q[1];
swap q[15], q[31];
swap q[0], q[25];
id q[30];
