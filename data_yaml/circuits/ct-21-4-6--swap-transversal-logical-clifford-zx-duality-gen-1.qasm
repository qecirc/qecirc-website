OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

swap q[15], q[18];
swap q[20], q[19];
swap q[9], q[7];
swap q[10], q[8];
id q[0];
swap q[1], q[18];
swap q[2], q[19];
swap q[3], q[15];
swap q[4], q[20];
swap q[11], q[7];
swap q[12], q[8];
swap q[13], q[9];
swap q[14], q[10];
swap q[5], q[1];
swap q[6], q[2];
swap q[16], q[11];
swap q[17], q[12];
