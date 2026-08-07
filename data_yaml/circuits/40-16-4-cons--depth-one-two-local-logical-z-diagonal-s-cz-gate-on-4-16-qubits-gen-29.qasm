OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[6];
s q[5];
s q[22];
s q[20];
s q[21];
s q[19];
s q[35];
s q[36];
id q[39];
cz q[6], q[5];
cz q[22], q[20];
cz q[21], q[19];
cz q[35], q[36];
