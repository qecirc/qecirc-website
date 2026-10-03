OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

swap q[14], q[3];
swap q[9], q[6];
swap q[0], q[12];
swap q[15], q[4];
swap q[10], q[7];
swap q[1], q[13];
