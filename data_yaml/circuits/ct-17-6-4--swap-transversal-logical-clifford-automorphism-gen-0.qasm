OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[4];
z q[3];
swap q[15], q[16];
swap q[5], q[6];
swap q[7], q[8];
swap q[10], q[11];
id q[0];
