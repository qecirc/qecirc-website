OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[4];
z q[2];
z q[1];
z q[13];
swap q[6], q[5];
swap q[9], q[8];
swap q[13], q[5];
swap q[3], q[8];
swap q[10], q[13];
swap q[0], q[3];
swap q[12], q[5];
swap q[2], q[8];
swap q[11], q[13];
swap q[1], q[3];
swap q[4], q[11];
swap q[7], q[1];
