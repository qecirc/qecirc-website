OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[10];
s q[2];
s q[23];
s q[22];
s q[5];
s q[13];
s q[20];
s q[21];
cz q[10], q[2];
cz q[23], q[21];
cz q[22], q[20];
cz q[5], q[13];
