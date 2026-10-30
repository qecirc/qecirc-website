OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

swap q[24], q[6];
swap q[16], q[13];
swap q[9], q[17];
swap q[8], q[11];
swap q[7], q[14];
swap q[4], q[1];
swap q[2], q[25];
swap q[30], q[21];
swap q[28], q[15];
swap q[29], q[19];
swap q[3], q[26];
swap q[22], q[12];
swap q[18], q[27];
swap q[31], q[20];
