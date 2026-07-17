OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[3];
z q[7];
swap q[13], q[10];
swap q[5], q[1];
swap q[8], q[11];
id q[0];
swap q[3], q[7];
