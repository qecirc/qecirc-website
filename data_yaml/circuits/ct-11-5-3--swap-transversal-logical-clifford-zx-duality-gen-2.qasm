OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[2];
x q[7];
z q[10];
x q[8];
z q[9];
x q[3];
h q[6];
h q[4];
h q[1];
h q[0];
h q[5];
h q[2];
h q[7];
h q[10];
h q[8];
h q[9];
h q[3];
swap q[9], q[3];
swap q[0], q[10];
swap q[5], q[9];
swap q[2], q[0];
swap q[4], q[10];
swap q[8], q[9];
