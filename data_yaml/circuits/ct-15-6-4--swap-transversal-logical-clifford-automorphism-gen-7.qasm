OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

swap q[14], q[6];
swap q[4], q[9];
swap q[11], q[7];
swap q[1], q[10];
id q[0];
swap q[12], q[14];
swap q[2], q[4];
swap q[13], q[11];
swap q[3], q[1];
