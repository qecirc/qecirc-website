OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[5];
z q[9];
swap q[15], q[12];
swap q[7], q[3];
swap q[10], q[13];
id q[0];
swap q[5], q[9];
