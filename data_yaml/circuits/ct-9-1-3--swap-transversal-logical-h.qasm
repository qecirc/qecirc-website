OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];

z q[5];
z q[4];
h q[6];
h q[7];
h q[8];
id q[0];
h q[5];
h q[4];
swap q[7], q[8];
swap q[4], q[8];
swap q[5], q[4];
