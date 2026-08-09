OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[10];
s q[9];
s q[31];
s q[28];
s q[30];
s q[27];
s q[29];
s q[32];
id q[39];
cz q[10], q[9];
cz q[31], q[28];
cz q[30], q[27];
cz q[29], q[32];
