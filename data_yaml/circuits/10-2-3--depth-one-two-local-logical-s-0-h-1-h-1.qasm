OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];

s q[4];
s q[2];
s q[8];
s q[9];
s q[7];
cz q[1], q[5];
cz q[2], q[8];
cz q[9], q[7];
