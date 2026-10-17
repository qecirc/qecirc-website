OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[12];
s q[6];
s q[1];
s q[22];
s q[0];
s q[21];
s q[11];
s q[35];
id q[39];
cz q[12], q[6];
cz q[1], q[22];
cz q[0], q[21];
cz q[11], q[35];
