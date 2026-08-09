OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

swap q[15], q[11];
swap q[17], q[13];
swap q[4], q[2];
swap q[5], q[3];
swap q[10], q[18];
swap q[12], q[8];
id q[0];
swap q[9], q[11];
swap q[1], q[13];
swap q[6], q[2];
swap q[7], q[3];
swap q[14], q[18];
swap q[16], q[8];
