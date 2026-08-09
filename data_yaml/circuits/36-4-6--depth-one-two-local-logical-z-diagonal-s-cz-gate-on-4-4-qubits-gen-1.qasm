OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

cz q[24], q[27];
cz q[19], q[30];
cz q[15], q[18];
cz q[12], q[26];
cz q[11], q[34];
cz q[10], q[31];
cz q[9], q[22];
cz q[8], q[29];
cz q[7], q[14];
cz q[6], q[23];
cz q[5], q[16];
cz q[4], q[33];
cz q[3], q[13];
cz q[2], q[28];
cz q[1], q[21];
cz q[0], q[20];
cz q[35], q[25];
cz q[32], q[17];
