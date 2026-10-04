OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[12];
s q[10];
s q[1];
s q[31];
s q[0];
s q[30];
s q[11];
s q[29];
id q[39];
cz q[12], q[10];
cz q[1], q[31];
cz q[0], q[30];
cz q[11], q[29];
