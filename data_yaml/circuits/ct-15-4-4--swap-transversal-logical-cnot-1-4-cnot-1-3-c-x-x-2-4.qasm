OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[7];
z q[14];
z q[6];
z q[13];
z q[4];
z q[11];
swap q[3], q[9];
swap q[5], q[12];
id q[0];
swap q[6], q[13];
swap q[7], q[14];
