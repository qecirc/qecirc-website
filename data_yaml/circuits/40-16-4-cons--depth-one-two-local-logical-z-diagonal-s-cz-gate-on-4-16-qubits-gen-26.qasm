OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[9];
s q[8];
s q[28];
s q[26];
s q[27];
s q[25];
s q[32];
s q[33];
id q[39];
cz q[9], q[8];
cz q[28], q[26];
cz q[27], q[25];
cz q[32], q[33];
