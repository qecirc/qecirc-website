OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

z q[10];
z q[8];
z q[6];
z q[5];
z q[3];
z q[2];
z q[15];
z q[16];
swap q[13], q[9];
swap q[4], q[17];
id q[0];
swap q[2], q[11];
swap q[3], q[15];
swap q[5], q[14];
swap q[6], q[13];
swap q[10], q[4];
swap q[7], q[2];
swap q[8], q[3];
swap q[12], q[5];
