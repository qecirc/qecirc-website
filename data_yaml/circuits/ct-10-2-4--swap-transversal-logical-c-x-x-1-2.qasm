OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[8];
z q[4];
z q[2];
x q[9];
z q[1];
z q[5];
h q[7];
h q[3];
h q[8];
h q[4];
h q[2];
h q[9];
swap q[1], q[0];
swap q[4], q[3];
swap q[7], q[2];
swap q[8], q[9];
