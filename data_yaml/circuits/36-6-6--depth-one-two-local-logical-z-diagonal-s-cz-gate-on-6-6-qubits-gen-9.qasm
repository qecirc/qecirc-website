OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

s q[29];
s q[23];
s q[26];
s q[20];
s q[12];
s q[15];
cz q[24], q[10];
cz q[18], q[11];
cz q[17], q[13];
cz q[35], q[16];
cz q[9], q[32];
cz q[7], q[33];
cz q[6], q[21];
cz q[5], q[4];
cz q[8], q[27];
cz q[3], q[34];
cz q[2], q[14];
cz q[1], q[19];
cz q[28], q[25];
cz q[22], q[0];
cz q[31], q[30];
