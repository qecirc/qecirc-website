OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];

z q[2];
z q[1];
x q[4];
x q[5];
h q[3];
sx q[0];
s q[2];
h q[1];
sx q[4];
sx q[5];
swap q[1], q[4];
swap q[2], q[1];
swap q[3], q[2];
