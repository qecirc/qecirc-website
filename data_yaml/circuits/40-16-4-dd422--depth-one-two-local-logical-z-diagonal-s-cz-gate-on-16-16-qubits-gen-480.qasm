OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[2];
s q[32];
s q[23];
s q[13];
s q[0];
s q[30];
s q[21];
s q[11];
cz q[20], q[8];
cz q[10], q[38];
cz q[9], q[29];
cz q[39], q[19];
cz q[7], q[3];
cz q[37], q[33];
cz q[28], q[24];
cz q[18], q[14];
cz q[6], q[4];
cz q[36], q[34];
cz q[27], q[25];
cz q[17], q[15];
cz q[5], q[1];
cz q[35], q[31];
cz q[26], q[22];
cz q[16], q[12];
