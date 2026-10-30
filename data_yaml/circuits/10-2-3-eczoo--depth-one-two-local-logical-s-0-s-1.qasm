OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

s q[8];
s q[7];
s q[4];
s q[9];
s q[6];
s q[3];
cz q[5], q[1];
cz q[2], q[0];
