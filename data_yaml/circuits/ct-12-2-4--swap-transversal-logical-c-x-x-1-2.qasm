OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[10];
z q[6];
z q[4];
x q[11];
z q[3];
z q[7];
h q[9];
h q[5];
id q[0];
h q[10];
h q[6];
h q[4];
h q[11];
swap q[3], q[2];
swap q[6], q[5];
swap q[9], q[4];
swap q[10], q[11];
