OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

swap q[24], q[5];
swap q[18], q[6];
swap q[17], q[7];
swap q[35], q[8];
swap q[13], q[10];
swap q[9], q[12];
swap q[32], q[14];
swap q[29], q[2];
swap q[23], q[15];
swap q[4], q[28];
swap q[21], q[1];
swap q[33], q[22];
swap q[27], q[31];
swap q[3], q[26];
swap q[0], q[25];
id q[30];
