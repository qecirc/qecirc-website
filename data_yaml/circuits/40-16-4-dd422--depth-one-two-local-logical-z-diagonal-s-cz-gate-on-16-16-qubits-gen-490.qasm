OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[28];
s q[18];
s q[25];
s q[15];
s q[24];
s q[14];
s q[23];
s q[13];
cz q[20], q[38];
cz q[10], q[8];
cz q[9], q[29];
cz q[39], q[19];
cz q[7], q[37];
cz q[6], q[35];
cz q[36], q[5];
cz q[27], q[26];
cz q[17], q[16];
cz q[4], q[34];
cz q[3], q[33];
cz q[2], q[32];
cz q[1], q[30];
cz q[31], q[0];
cz q[22], q[21];
cz q[12], q[11];
