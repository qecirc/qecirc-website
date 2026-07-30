OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[1], q[0];
swap q[2], q[13];
swap q[3], q[11];
swap q[8], q[7];
swap q[9], q[6];
swap q[10], q[5];
swap q[12], q[4];
