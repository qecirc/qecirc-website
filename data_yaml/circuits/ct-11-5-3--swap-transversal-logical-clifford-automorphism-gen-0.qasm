OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[4];
x q[7];
x q[10];
x q[9];
s q[6];
sx q[2];
h q[1];
s q[0];
s q[8];
h q[5];
h q[3];
s q[4];
sx q[7];
h q[10];
sx q[9];
swap q[5], q[3];
swap q[8], q[5];
swap q[7], q[0];
swap q[1], q[0];
swap q[6], q[8];
swap q[2], q[0];
