OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[7];
z q[11];
z q[2];
x q[6];
z q[1];
x q[5];
z q[12];
s q[4];
s q[3];
s q[10];
h q[13];
h q[9];
sx q[8];
id q[0];
h q[7];
s q[11];
h q[2];
h q[6];
sx q[1];
sx q[5];
sx q[12];
swap q[4], q[10];
swap q[1], q[5];
swap q[6], q[13];
