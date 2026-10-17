OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

swap q[3], q[2];
swap q[23], q[22];
swap q[19], q[18];
swap q[16], q[14];
swap q[15], q[13];
swap q[9], q[8];
id q[5];
