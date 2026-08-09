OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

swap q[18], q[10];
swap q[13], q[15];
swap q[19], q[21];
id q[0];
swap q[14], q[10];
swap q[20], q[15];
swap q[12], q[21];
swap q[17], q[10];
swap q[1], q[15];
swap q[2], q[21];
swap q[3], q[10];
swap q[4], q[15];
swap q[5], q[21];
swap q[6], q[10];
swap q[7], q[15];
swap q[8], q[21];
swap q[9], q[10];
swap q[11], q[15];
swap q[16], q[21];
