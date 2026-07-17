OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[8];
z q[5];
z q[1];
z q[13];
swap q[14], q[4];
swap q[9], q[7];
swap q[15], q[3];
swap q[10], q[6];
swap q[0], q[13];
swap q[1], q[12];
