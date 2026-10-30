OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[7], q[6];
swap q[3], q[12];
swap q[2], q[4];
swap q[1], q[9];
swap q[0], q[13];
swap q[11], q[8];
