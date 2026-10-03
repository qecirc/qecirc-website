OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

swap q[12], q[3];
swap q[10], q[41];
swap q[9], q[36];
swap q[8], q[32];
swap q[7], q[28];
swap q[6], q[24];
swap q[5], q[20];
swap q[4], q[16];
id q[47];
