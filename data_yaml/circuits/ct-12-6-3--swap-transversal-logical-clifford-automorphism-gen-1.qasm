OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[7];
y q[10];
z q[6];
x q[8];
s q[3];
h q[2];
h q[1];
h q[0];
h q[11];
h q[4];
h q[5];
h q[9];
s q[7];
h q[10];
h q[6];
h q[8];
swap q[1], q[0];
swap q[2], q[11];
swap q[6], q[8];
swap q[7], q[3];
