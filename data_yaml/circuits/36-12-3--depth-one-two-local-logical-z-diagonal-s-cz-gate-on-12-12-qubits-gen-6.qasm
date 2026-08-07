OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

cz q[28], q[31];
cz q[20], q[22];
cz q[16], q[18];
cz q[12], q[14];
cz q[8], q[10];
cz q[6], q[11];
cz q[5], q[15];
cz q[4], q[19];
cz q[3], q[24];
cz q[2], q[30];
cz q[1], q[33];
cz q[0], q[26];
cz q[13], q[27];
cz q[17], q[35];
cz q[9], q[32];
cz q[7], q[23];
cz q[29], q[34];
cz q[21], q[25];
