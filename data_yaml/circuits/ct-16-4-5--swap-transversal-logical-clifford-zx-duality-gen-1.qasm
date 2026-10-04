OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[6];
z q[5];
z q[2];
z q[9];
z q[7];
z q[14];
swap q[11], q[13];
swap q[15], q[7];
swap q[12], q[9];
swap q[2], q[11];
swap q[0], q[15];
swap q[1], q[12];
swap q[5], q[2];
swap q[3], q[0];
swap q[4], q[1];
swap q[10], q[5];
swap q[6], q[3];
swap q[8], q[4];
