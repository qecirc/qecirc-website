OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

z q[6];
z q[1];
z q[5];
z q[12];
z q[8];
z q[4];
z q[11];
swap q[2], q[10];
swap q[3], q[9];
swap q[11], q[7];
swap q[0], q[4];
