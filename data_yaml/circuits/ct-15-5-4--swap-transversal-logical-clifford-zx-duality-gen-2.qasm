OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[5];
z q[2];
z q[4];
z q[12];
z q[11];
z q[10];
swap q[14], q[13];
id q[0];
swap q[4], q[11];
swap q[6], q[12];
swap q[2], q[1];
swap q[7], q[14];
swap q[3], q[11];
swap q[5], q[12];
swap q[9], q[2];
