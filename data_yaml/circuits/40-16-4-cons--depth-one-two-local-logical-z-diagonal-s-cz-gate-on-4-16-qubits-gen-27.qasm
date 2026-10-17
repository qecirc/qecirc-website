OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[8];
s q[7];
s q[26];
s q[24];
s q[25];
s q[23];
s q[33];
s q[34];
id q[39];
cz q[8], q[7];
cz q[26], q[24];
cz q[25], q[23];
cz q[33], q[34];
