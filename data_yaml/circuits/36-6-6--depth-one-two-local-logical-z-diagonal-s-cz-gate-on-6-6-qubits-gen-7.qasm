OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

s q[3];
s q[34];
s q[26];
s q[20];
cz q[24], q[22];
cz q[18], q[1];
cz q[17], q[28];
cz q[35], q[31];
cz q[13], q[25];
cz q[11], q[19];
cz q[10], q[0];
cz q[16], q[30];
cz q[9], q[2];
cz q[32], q[14];
cz q[29], q[12];
cz q[23], q[15];
cz q[7], q[4];
cz q[6], q[21];
cz q[5], q[33];
cz q[8], q[27];
