OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[8];
z q[4];
swap q[7], q[5];
swap q[9], q[3];
swap q[10], q[2];
swap q[11], q[16];
swap q[13], q[14];
swap q[15], q[12];
id q[0];
swap q[8], q[4];
