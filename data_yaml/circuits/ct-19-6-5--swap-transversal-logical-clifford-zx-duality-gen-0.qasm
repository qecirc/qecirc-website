OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

swap q[17], q[11];
swap q[9], q[13];
swap q[1], q[15];
swap q[5], q[2];
swap q[6], q[3];
swap q[7], q[4];
swap q[12], q[18];
swap q[14], q[8];
swap q[16], q[10];
id q[0];
