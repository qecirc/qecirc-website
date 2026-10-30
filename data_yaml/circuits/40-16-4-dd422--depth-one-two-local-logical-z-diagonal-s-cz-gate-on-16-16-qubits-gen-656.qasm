OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[36];
s q[17];
s q[34];
s q[15];
cz q[20], q[26];
cz q[10], q[35];
cz q[9], q[5];
cz q[39], q[16];
cz q[8], q[28];
cz q[38], q[37];
cz q[29], q[7];
cz q[19], q[18];
cz q[6], q[27];
cz q[4], q[25];
cz q[3], q[22];
cz q[33], q[31];
cz q[24], q[1];
cz q[14], q[12];
cz q[2], q[21];
cz q[32], q[30];
cz q[23], q[0];
cz q[13], q[11];
