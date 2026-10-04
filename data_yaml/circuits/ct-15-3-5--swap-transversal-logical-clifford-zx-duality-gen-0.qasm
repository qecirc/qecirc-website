OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[6];
z q[2];
swap q[5], q[3];
swap q[7], q[1];
swap q[8], q[0];
swap q[9], q[14];
swap q[11], q[12];
swap q[13], q[10];
swap q[6], q[2];
