OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[5];
z q[12];
z q[2];
z q[6];
z q[13];
z q[9];
id q[0];
swap q[10], q[13];
swap q[14], q[9];
swap q[7], q[2];
swap q[3], q[6];
swap q[12], q[7];
swap q[11], q[3];
swap q[4], q[10];
swap q[5], q[14];
