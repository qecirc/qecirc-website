OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

swap q[18], q[14];
swap q[20], q[16];
swap q[7], q[5];
swap q[8], q[6];
swap q[13], q[21];
swap q[15], q[11];
id q[0];
swap q[12], q[18];
swap q[4], q[20];
swap q[9], q[7];
swap q[10], q[8];
swap q[17], q[13];
swap q[19], q[15];
