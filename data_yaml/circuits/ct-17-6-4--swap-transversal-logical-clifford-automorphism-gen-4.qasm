OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

swap q[11], q[8];
swap q[12], q[9];
swap q[6], q[16];
swap q[3], q[13];
id q[0];
