OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

s q[29];
s q[23];
s q[33];
s q[27];
s q[19];
s q[30];
cz q[24], q[10];
cz q[18], q[11];
cz q[17], q[13];
cz q[35], q[16];
cz q[9], q[32];
cz q[7], q[26];
cz q[6], q[34];
cz q[5], q[3];
cz q[8], q[20];
cz q[4], q[21];
cz q[2], q[22];
cz q[14], q[28];
cz q[12], q[1];
cz q[15], q[31];
cz q[0], q[25];
