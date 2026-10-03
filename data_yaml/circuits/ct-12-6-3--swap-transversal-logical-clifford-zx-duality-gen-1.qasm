OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[3];
z q[2];
z q[1];
x q[11];
z q[4];
y q[10];
x q[5];
x q[9];
h q[7];
h q[0];
h q[6];
h q[8];
h q[3];
h q[2];
h q[1];
h q[11];
h q[4];
h q[10];
h q[5];
h q[9];
swap q[4], q[8];
swap q[0], q[11];
swap q[1], q[5];
swap q[2], q[9];
