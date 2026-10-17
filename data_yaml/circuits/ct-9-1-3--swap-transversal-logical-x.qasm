OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

z q[5];
z q[4];
h q[6];
s q[7];
s q[8];
id q[0];
s q[5];
s q[4];
swap q[5], q[4];
