OPENQASM 2.0;
include "qelib1.inc";

qreg q[6];

z q[2];
z q[1];
h q[3];
h q[4];
h q[5];
id q[0];
h q[2];
h q[1];
swap q[4], q[5];
swap q[1], q[4];
swap q[2], q[4];
