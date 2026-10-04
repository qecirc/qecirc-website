OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[3];
z q[14];
z q[9];
swap q[10], q[7];
swap q[1], q[11];
id q[0];
swap q[4], q[14];
swap q[12], q[1];
swap q[2], q[11];
swap q[8], q[5];
swap q[13], q[14];
swap q[3], q[4];
