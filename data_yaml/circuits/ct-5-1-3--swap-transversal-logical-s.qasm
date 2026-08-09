OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];

z q[2];
z q[1];
x q[3];
y q[4];
h q[0];
sx q[2];
h q[1];
h q[3];
h q[4];
swap q[1], q[0];
