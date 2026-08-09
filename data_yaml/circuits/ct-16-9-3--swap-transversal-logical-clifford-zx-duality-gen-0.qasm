OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

swap q[4], q[13];
swap q[12], q[6];
swap q[15], q[10];
swap q[1], q[7];
swap q[3], q[11];
swap q[5], q[14];
id q[0];
