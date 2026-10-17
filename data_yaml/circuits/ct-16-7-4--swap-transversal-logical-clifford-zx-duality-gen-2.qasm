OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

z q[4];
z q[2];
z q[7];
z q[11];
swap q[8], q[15];
swap q[13], q[3];
swap q[6], q[14];
swap q[12], q[1];
swap q[9], q[11];
swap q[10], q[7];
swap q[2], q[5];
swap q[4], q[0];
