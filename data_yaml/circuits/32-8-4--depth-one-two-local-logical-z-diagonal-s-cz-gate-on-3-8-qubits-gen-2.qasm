OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

s q[24];
s q[18];
s q[9];
s q[8];
s q[7];
s q[6];
s q[2];
s q[30];
s q[25];
s q[26];
s q[27];
s q[29];
id q[21];
cz q[24], q[26];
cz q[18], q[30];
cz q[9], q[29];
cz q[8], q[27];
cz q[7], q[2];
cz q[6], q[25];
