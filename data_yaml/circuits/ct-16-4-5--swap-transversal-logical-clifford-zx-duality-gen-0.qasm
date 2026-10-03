OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[8];
z q[6];
z q[4];
z q[3];
z q[1];
z q[0];
z q[13];
z q[14];
swap q[11], q[7];
swap q[2], q[15];
swap q[0], q[9];
swap q[1], q[13];
swap q[3], q[12];
swap q[4], q[11];
swap q[8], q[2];
swap q[5], q[0];
swap q[6], q[1];
swap q[10], q[3];
