OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

swap q[11], q[3];
swap q[6], q[13];
swap q[4], q[10];
swap q[5], q[17];
swap q[2], q[9];
swap q[1], q[7];
swap q[0], q[8];
swap q[14], q[15];
