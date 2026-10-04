OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[8];
z q[3];
z q[14];
z q[9];
id q[0];
swap q[9], q[6];
swap q[4], q[14];
swap q[3], q[13];
swap q[8], q[5];
