OPENQASM 2.0;
include "qelib1.inc";

qreg q[7];

z q[3];
z q[0];
z q[4];
s q[1];
s q[5];
s q[2];
s q[6];
s q[3];
s q[0];
s q[4];
