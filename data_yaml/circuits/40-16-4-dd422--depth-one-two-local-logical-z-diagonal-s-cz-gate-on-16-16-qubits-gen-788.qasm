OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[27];
s q[17];
s q[25];
s q[15];
s q[23];
s q[13];
s q[21];
s q[11];
cz q[20], q[38];
cz q[10], q[8];
cz q[9], q[29];
cz q[39], q[19];
cz q[7], q[35];
cz q[37], q[5];
cz q[28], q[26];
cz q[18], q[16];
cz q[6], q[36];
cz q[4], q[34];
cz q[3], q[31];
cz q[33], q[1];
cz q[24], q[22];
cz q[14], q[12];
cz q[2], q[32];
cz q[0], q[30];
