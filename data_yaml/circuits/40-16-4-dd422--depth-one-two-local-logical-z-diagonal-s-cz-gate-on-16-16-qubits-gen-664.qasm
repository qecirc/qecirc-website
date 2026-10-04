OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[3];
s q[33];
s q[2];
s q[32];
s q[1];
s q[31];
s q[0];
s q[30];
cz q[20], q[5];
cz q[10], q[35];
cz q[9], q[16];
cz q[39], q[26];
cz q[8], q[4];
cz q[38], q[34];
cz q[29], q[15];
cz q[19], q[25];
cz q[7], q[6];
cz q[37], q[36];
cz q[28], q[17];
cz q[18], q[27];
cz q[24], q[14];
cz q[23], q[13];
cz q[22], q[12];
cz q[21], q[11];
