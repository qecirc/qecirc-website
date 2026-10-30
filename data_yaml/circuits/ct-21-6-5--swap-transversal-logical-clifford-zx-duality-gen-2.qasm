OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

swap q[17], q[13];
swap q[19], q[15];
swap q[6], q[4];
swap q[7], q[5];
swap q[12], q[20];
swap q[14], q[10];
id q[0];
swap q[11], q[13];
swap q[3], q[15];
swap q[8], q[4];
swap q[9], q[5];
swap q[16], q[20];
swap q[18], q[10];
