OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[10];
s q[6];
s q[31];
s q[22];
s q[30];
s q[21];
s q[29];
s q[35];
id q[39];
cz q[10], q[6];
cz q[31], q[22];
cz q[30], q[21];
cz q[29], q[35];
