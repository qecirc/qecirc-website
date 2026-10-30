OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

swap q[24], q[13];
swap q[16], q[11];
swap q[10], q[7];
swap q[9], q[6];
swap q[8], q[4];
swap q[2], q[1];
swap q[0], q[17];
swap q[14], q[25];
swap q[30], q[31];
swap q[28], q[23];
swap q[29], q[21];
swap q[3], q[18];
swap q[22], q[26];
swap q[19], q[5];
swap q[15], q[27];
swap q[12], q[20];
