OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[1];
z q[4];
z q[7];
swap q[10], q[6];
id q[0];
swap q[7], q[9];
swap q[4], q[10];
swap q[2], q[6];
swap q[14], q[7];
swap q[11], q[4];
swap q[12], q[9];
swap q[1], q[14];
swap q[13], q[11];
swap q[3], q[1];
swap q[8], q[13];
swap q[5], q[3];
