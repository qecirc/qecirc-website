OPENQASM 2.0;
include "qelib1.inc";

qreg q[11];

z q[3];
z q[2];
x q[9];
x q[6];
y q[7];
h q[8];
h q[5];
sx q[10];
h q[1];
h q[4];
sx q[0];
sx q[3];
sx q[2];
sx q[9];
s q[6];
s q[7];
swap q[5], q[1];
swap q[8], q[4];
swap q[3], q[10];
