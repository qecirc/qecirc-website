OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];

z q[3];
z q[2];
z q[1];
z q[4];
s q[0];
sx q[3];
sx q[2];
h q[1];
h q[4];
swap q[1], q[0];
swap q[2], q[0];
swap q[3], q[1];
