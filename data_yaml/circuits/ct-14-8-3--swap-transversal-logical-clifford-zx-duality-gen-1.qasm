OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[10];
z q[0];
z q[4];
swap q[13], q[11];
swap q[6], q[4];
swap q[9], q[13];
swap q[2], q[6];
swap q[12], q[9];
swap q[5], q[2];
swap q[7], q[12];
swap q[0], q[5];
swap q[8], q[7];
swap q[1], q[0];
swap q[10], q[8];
swap q[3], q[1];
