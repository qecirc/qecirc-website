OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

z q[16];
z q[13];
z q[11];
z q[9];
z q[8];
z q[6];
swap q[14], q[17];
swap q[19], q[18];
swap q[0], q[14];
swap q[1], q[19];
swap q[8], q[6];
swap q[9], q[7];
swap q[2], q[0];
swap q[3], q[1];
swap q[10], q[8];
swap q[11], q[9];
swap q[4], q[2];
swap q[5], q[3];
swap q[12], q[10];
swap q[13], q[11];
swap q[15], q[12];
swap q[16], q[13];
