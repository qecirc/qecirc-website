OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[6];
s q[4];
s q[3];
s q[2];
s q[5];
s q[9];
s q[20];
s q[21];
cz q[6], q[9];
cz q[4], q[3];
cz q[2], q[5];
cz q[20], q[21];
