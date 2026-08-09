OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[11];
s q[20];
s q[32];
s q[36];
s q[35];
s q[29];
s q[0];
s q[13];
cz q[28], q[4];
cz q[22], q[31];
cz q[21], q[38];
cz q[39], q[23];
cz q[15], q[12];
cz q[9], q[2];
cz q[8], q[14];
cz q[7], q[17];
cz q[10], q[18];
cz q[6], q[26];
cz q[25], q[1];
cz q[37], q[34];
cz q[30], q[33];
cz q[5], q[24];
cz q[3], q[27];
cz q[19], q[16];
