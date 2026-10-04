OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

swap q[16], q[5];
swap q[11], q[8];
swap q[2], q[14];
swap q[17], q[6];
swap q[12], q[9];
swap q[3], q[15];
id q[0];
