OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];

z q[11];
z q[7];
z q[5];
x q[12];
z q[4];
z q[8];
h q[10];
h q[6];
id q[0];
h q[11];
h q[7];
h q[5];
h q[12];
swap q[4], q[3];
swap q[7], q[6];
swap q[10], q[5];
swap q[11], q[12];
