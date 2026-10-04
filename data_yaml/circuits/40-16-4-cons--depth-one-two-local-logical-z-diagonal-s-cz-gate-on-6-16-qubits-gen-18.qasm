OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[12];
s q[5];
s q[1];
s q[20];
s q[0];
s q[19];
s q[11];
s q[36];
id q[39];
cz q[12], q[5];
cz q[1], q[20];
cz q[0], q[19];
cz q[11], q[36];
