OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

swap q[12], q[10];
swap q[3], q[41];
swap q[2], q[40];
swap q[1], q[39];
swap q[0], q[38];
swap q[11], q[37];
id q[47];
