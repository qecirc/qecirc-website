OPENQASM 2.0;
include "qelib1.inc";

qreg q[80];

swap q[16], q[14];
swap q[5], q[71];
swap q[4], q[70];
swap q[3], q[69];
swap q[2], q[68];
swap q[1], q[67];
swap q[0], q[66];
swap q[15], q[65];
id q[79];
