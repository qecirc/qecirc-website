OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[6];
z q[4];
z q[8];
z q[7];
swap q[15], q[11];
swap q[13], q[12];
swap q[3], q[2];
id q[0];
swap q[5], q[8];
swap q[14], q[15];
swap q[6], q[2];
swap q[9], q[12];
swap q[4], q[5];
