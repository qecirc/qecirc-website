OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

swap q[11], q[4];
swap q[3], q[17];
swap q[10], q[5];
swap q[13], q[12];
swap q[2], q[14];
swap q[1], q[15];
swap q[0], q[16];
swap q[7], q[9];
