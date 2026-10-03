OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

s q[24];
s q[19];
s q[16];
s q[13];
s q[10];
s q[8];
s q[26];
s q[21];
s q[4];
s q[2];
s q[0];
s q[5];
s q[28];
s q[30];
s q[23];
s q[15];
cz q[24], q[30];
cz q[19], q[0];
cz q[16], q[23];
cz q[13], q[5];
cz q[10], q[15];
cz q[8], q[4];
cz q[26], q[28];
cz q[21], q[2];
