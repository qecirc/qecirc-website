OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

swap q[5], q[6];
swap q[8], q[9];
swap q[14], q[15];
swap q[17], q[16];
swap q[12], q[11];
swap q[3], q[2];
id q[0];
