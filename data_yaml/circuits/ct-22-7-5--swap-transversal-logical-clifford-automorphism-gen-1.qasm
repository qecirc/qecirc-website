OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

swap q[20], q[10];
swap q[12], q[15];
swap q[17], q[21];
swap q[1], q[18];
swap q[2], q[13];
swap q[3], q[19];
swap q[4], q[14];
id q[0];
swap q[5], q[20];
swap q[6], q[12];
swap q[7], q[17];
swap q[8], q[1];
swap q[9], q[2];
swap q[11], q[3];
swap q[16], q[4];
