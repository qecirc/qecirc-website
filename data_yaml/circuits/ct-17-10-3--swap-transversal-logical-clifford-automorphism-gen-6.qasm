OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

swap q[15], q[4];
swap q[10], q[7];
swap q[1], q[13];
swap q[16], q[5];
swap q[11], q[8];
swap q[2], q[14];
id q[0];
