OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[11];
z q[5];
z q[4];
z q[3];
z q[6];
z q[12];
swap q[16], q[15];
swap q[7], q[8];
id q[0];
swap q[4], q[3];
swap q[5], q[6];
