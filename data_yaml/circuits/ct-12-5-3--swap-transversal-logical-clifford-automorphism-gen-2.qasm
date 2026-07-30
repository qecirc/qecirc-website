OPENQASM 2.0;
include "qelib1.inc";

qreg q[12];

z q[5];
z q[3];
x q[11];
z q[9];
z q[6];
sx q[7];
h q[2];
s q[8];
sx q[1];
s q[10];
h q[4];
sx q[0];
h q[5];
sx q[3];
s q[11];
s q[9];
sx q[6];
swap q[10], q[4];
swap q[8], q[1];
swap q[9], q[4];
swap q[3], q[1];
swap q[5], q[1];
swap q[7], q[9];
