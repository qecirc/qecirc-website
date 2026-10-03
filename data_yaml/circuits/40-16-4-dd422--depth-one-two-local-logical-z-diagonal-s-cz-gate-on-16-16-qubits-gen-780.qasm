OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[7];
s q[18];
s q[2];
s q[13];
s q[1];
s q[12];
s q[0];
s q[11];
cz q[20], q[3];
cz q[10], q[24];
cz q[9], q[33];
cz q[39], q[14];
cz q[8], q[4];
cz q[38], q[25];
cz q[29], q[34];
cz q[19], q[15];
cz q[37], q[28];
cz q[6], q[5];
cz q[36], q[26];
cz q[27], q[35];
cz q[17], q[16];
cz q[32], q[23];
cz q[31], q[22];
cz q[30], q[21];
