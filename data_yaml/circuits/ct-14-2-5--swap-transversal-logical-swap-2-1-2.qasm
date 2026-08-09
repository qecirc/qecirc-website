OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

swap q[5], q[11];
swap q[6], q[13];
swap q[7], q[0];
swap q[8], q[1];
swap q[9], q[2];
swap q[10], q[3];
swap q[12], q[4];
