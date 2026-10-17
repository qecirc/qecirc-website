OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[4];
z q[3];
z q[11];
z q[10];
id q[0];
swap q[8], q[10];
swap q[11], q[7];
swap q[14], q[3];
swap q[4], q[13];
