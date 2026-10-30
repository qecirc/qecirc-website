OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

z q[4];
x q[9];
z q[12];
x q[10];
z q[11];
x q[5];
h q[8];
h q[6];
h q[3];
h q[2];
h q[7];
id q[0];
h q[4];
h q[9];
h q[12];
h q[10];
h q[11];
h q[5];
swap q[11], q[5];
swap q[2], q[12];
swap q[7], q[11];
swap q[4], q[2];
swap q[6], q[12];
swap q[10], q[11];
