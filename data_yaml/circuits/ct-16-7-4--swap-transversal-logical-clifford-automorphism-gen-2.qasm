OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[1];
z q[0];
z q[10];
z q[13];
z q[7];
z q[11];
z q[3];
z q[15];
swap q[4], q[2];
swap q[12], q[6];
swap q[3], q[15];
swap q[7], q[11];
swap q[13], q[8];
swap q[10], q[9];
swap q[0], q[5];
swap q[1], q[14];
