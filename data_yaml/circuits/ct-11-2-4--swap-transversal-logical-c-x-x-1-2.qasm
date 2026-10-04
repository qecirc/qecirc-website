OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[9];
z q[5];
z q[3];
x q[10];
z q[2];
z q[6];
h q[8];
h q[4];
id q[0];
h q[9];
h q[5];
h q[3];
h q[10];
swap q[2], q[1];
swap q[5], q[4];
swap q[8], q[3];
swap q[9], q[10];
