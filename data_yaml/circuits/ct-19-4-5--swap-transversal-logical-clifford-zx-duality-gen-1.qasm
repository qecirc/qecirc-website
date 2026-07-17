OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

swap q[14], q[10];
swap q[3], q[12];
swap q[4], q[16];
swap q[5], q[18];
swap q[6], q[15];
id q[0];
swap q[7], q[14];
swap q[8], q[3];
swap q[9], q[4];
swap q[11], q[5];
swap q[13], q[6];
