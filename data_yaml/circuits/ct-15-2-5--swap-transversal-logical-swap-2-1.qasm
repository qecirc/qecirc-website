OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

swap q[6], q[12];
swap q[7], q[14];
swap q[8], q[1];
swap q[9], q[2];
swap q[10], q[3];
swap q[11], q[4];
swap q[13], q[5];
id q[0];
