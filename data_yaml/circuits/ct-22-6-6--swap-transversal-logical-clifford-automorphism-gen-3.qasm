OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

swap q[20], q[14];
swap q[12], q[16];
swap q[4], q[18];
swap q[8], q[5];
swap q[9], q[6];
swap q[10], q[7];
swap q[15], q[21];
swap q[17], q[11];
swap q[19], q[13];
id q[0];
