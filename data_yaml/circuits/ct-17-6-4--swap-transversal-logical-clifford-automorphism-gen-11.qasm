OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[4];
z q[8];
swap q[16], q[11];
swap q[13], q[12];
swap q[3], q[9];
id q[0];
swap q[6], q[8];
swap q[14], q[16];
swap q[7], q[9];
swap q[10], q[12];
swap q[4], q[6];
