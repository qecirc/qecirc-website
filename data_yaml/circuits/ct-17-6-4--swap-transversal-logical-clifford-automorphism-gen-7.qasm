OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[4];
z q[8];
swap q[14], q[11];
swap q[7], q[3];
swap q[10], q[13];
id q[0];
swap q[4], q[8];
