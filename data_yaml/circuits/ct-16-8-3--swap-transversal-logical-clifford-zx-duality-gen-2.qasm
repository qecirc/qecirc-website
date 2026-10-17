OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[12];
z q[10];
z q[11];
z q[2];
z q[4];
z q[8];
swap q[15], q[13];
id q[0];
swap q[8], q[6];
swap q[11], q[15];
swap q[9], q[13];
swap q[4], q[8];
swap q[2], q[6];
swap q[14], q[11];
swap q[10], q[15];
swap q[7], q[4];
swap q[3], q[8];
swap q[12], q[11];
swap q[5], q[4];
