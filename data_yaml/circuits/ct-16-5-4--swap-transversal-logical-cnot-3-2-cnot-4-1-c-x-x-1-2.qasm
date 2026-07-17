OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[10];
z q[4];
z q[3];
z q[2];
z q[5];
z q[11];
swap q[15], q[14];
swap q[6], q[7];
id q[0];
swap q[3], q[2];
swap q[4], q[5];
