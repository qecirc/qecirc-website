OPENQASM 2.0;
include "qelib1.inc";

qreg q[31];

s q[24];
s q[16];
s q[10];
s q[26];
s q[6];
s q[3];
s q[1];
s q[7];
s q[20];
s q[14];
s q[9];
s q[22];
s q[28];
s q[30];
s q[23];
s q[15];
cz q[24], q[22];
cz q[16], q[20];
cz q[10], q[14];
cz q[26], q[9];
cz q[6], q[15];
cz q[3], q[28];
cz q[1], q[30];
cz q[7], q[23];
