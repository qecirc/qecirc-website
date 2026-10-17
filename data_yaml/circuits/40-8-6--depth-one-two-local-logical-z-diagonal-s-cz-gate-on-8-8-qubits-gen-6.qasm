OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[22];
s q[39];
s q[9];
s q[10];
s q[27];
s q[29];
s q[34];
s q[33];
cz q[28], q[21];
cz q[15], q[25];
cz q[12], q[6];
cz q[11], q[37];
cz q[20], q[30];
cz q[8], q[7];
cz q[5], q[17];
cz q[32], q[2];
cz q[24], q[14];
cz q[36], q[18];
cz q[4], q[16];
cz q[38], q[19];
cz q[31], q[0];
cz q[23], q[13];
cz q[3], q[35];
cz q[1], q[26];
