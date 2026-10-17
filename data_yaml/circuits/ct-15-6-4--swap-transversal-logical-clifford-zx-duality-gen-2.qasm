OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[5];
z q[2];
z q[14];
z q[7];
swap q[9], q[6];
swap q[1], q[11];
id q[0];
swap q[2], q[12];
swap q[8], q[5];
