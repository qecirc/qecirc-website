OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[4];
z q[0];
swap q[13], q[5];
swap q[3], q[8];
swap q[2], q[10];
swap q[11], q[8];
swap q[1], q[5];
swap q[12], q[0];
swap q[7], q[2];
swap q[4], q[12];
