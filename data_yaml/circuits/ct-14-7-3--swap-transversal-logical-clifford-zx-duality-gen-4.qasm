OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[9], q[8];
swap q[13], q[12];
swap q[6], q[5];
swap q[2], q[1];
id q[0];
swap q[11], q[9];
swap q[10], q[13];
swap q[3], q[6];
swap q[4], q[2];
