OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[6];
z q[2];
z q[13];
z q[11];
swap q[5], q[12];
swap q[15], q[14];
id q[0];
swap q[7], q[13];
swap q[3], q[2];
swap q[4], q[5];
swap q[8], q[14];
swap q[6], q[7];
swap q[10], q[2];
