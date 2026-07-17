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
swap q[6], q[4];
swap q[12], q[2];
swap q[11], q[3];
swap q[7], q[15];
swap q[9], q[13];
swap q[10], q[8];
swap q[14], q[0];
swap q[1], q[5];
