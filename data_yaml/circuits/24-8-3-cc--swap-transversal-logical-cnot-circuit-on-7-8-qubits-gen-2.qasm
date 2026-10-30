OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

swap q[14], q[1];
swap q[9], q[0];
swap q[19], q[2];
swap q[18], q[13];
swap q[10], q[23];
swap q[20], q[15];
id q[21];
