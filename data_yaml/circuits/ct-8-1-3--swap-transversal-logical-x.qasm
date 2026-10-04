OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

z q[4];
z q[3];
x q[7];
h q[5];
s q[6];
id q[0];
s q[4];
h q[3];
sx q[7];
swap q[6], q[7];
swap q[4], q[7];
swap q[5], q[4];
