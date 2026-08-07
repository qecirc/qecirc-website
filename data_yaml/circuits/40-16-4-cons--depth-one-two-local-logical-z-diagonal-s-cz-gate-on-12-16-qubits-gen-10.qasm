OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[8];
s q[3];
s q[26];
s q[16];
s q[25];
s q[15];
s q[33];
s q[38];
id q[39];
cz q[8], q[3];
cz q[26], q[16];
cz q[25], q[15];
cz q[33], q[38];
