OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

swap q[3], q[2];
swap q[4], q[1];
swap q[5], q[14];
swap q[6], q[12];
swap q[10], q[9];
swap q[11], q[8];
swap q[13], q[7];
id q[0];
