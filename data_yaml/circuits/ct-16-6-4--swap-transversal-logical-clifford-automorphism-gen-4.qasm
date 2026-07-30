OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[6];
z q[4];
z q[3];
z q[2];
swap q[14], q[10];
swap q[9], q[15];
id q[0];
swap q[4], q[7];
swap q[6], q[5];
