OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

z q[1];
x q[3];
z q[5];
z q[6];
s q[7];
s q[4];
s q[2];
s q[8];
s q[9];
sx q[0];
s q[1];
sx q[3];
s q[5];
s q[6];
swap q[1], q[9];
swap q[4], q[6];
swap q[7], q[5];
