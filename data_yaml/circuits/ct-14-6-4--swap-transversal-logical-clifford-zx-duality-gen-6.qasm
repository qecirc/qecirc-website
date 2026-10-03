OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[0];
z q[5];
swap q[13], q[9];
swap q[3], q[6];
swap q[12], q[11];
swap q[2], q[1];
swap q[10], q[13];
swap q[0], q[3];
swap q[4], q[2];
swap q[7], q[12];
