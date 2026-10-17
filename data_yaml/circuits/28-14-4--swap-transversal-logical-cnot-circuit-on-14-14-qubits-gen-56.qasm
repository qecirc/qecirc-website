OPENQASM 2.0;
include "qelib1.inc";

qreg q[25];

swap q[12], q[13];
swap q[23], q[24];
swap q[19], q[20];
swap q[2], q[0];
swap q[16], q[17];
swap q[11], q[9];
id q[5];
