OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[9];
s q[4];
s q[28];
s q[18];
s q[27];
s q[17];
s q[32];
s q[37];
id q[39];
cz q[9], q[4];
cz q[28], q[18];
cz q[27], q[17];
cz q[32], q[37];
