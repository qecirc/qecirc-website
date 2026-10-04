OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[3];
z q[2];
z q[10];
x q[4];
h q[7];
h q[5];
h q[8];
h q[1];
h q[11];
h q[9];
h q[6];
id q[0];
h q[3];
h q[2];
h q[10];
h q[4];
swap q[5], q[1];
swap q[6], q[10];
swap q[2], q[8];
swap q[3], q[11];
