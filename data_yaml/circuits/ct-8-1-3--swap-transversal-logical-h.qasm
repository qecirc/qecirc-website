OPENQASM 2.0;
include "qelib1.inc";

qreg q[8];

z q[4];
z q[3];
h q[5];
h q[6];
h q[7];
id q[0];
h q[4];
h q[3];
swap q[6], q[7];
swap q[3], q[7];
swap q[4], q[3];
