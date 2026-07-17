OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[2];
z q[13];
swap q[3], q[12];
swap q[6], q[9];
swap q[0], q[14];
swap q[1], q[7];
swap q[4], q[10];
swap q[2], q[13];
