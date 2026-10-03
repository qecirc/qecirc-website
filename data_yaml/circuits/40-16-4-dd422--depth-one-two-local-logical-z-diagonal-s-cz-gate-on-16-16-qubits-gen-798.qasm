OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

cz q[20], q[10];
cz q[9], q[39];
cz q[8], q[38];
cz q[29], q[19];
cz q[7], q[37];
cz q[28], q[18];
cz q[6], q[36];
cz q[27], q[17];
cz q[5], q[34];
cz q[35], q[4];
cz q[26], q[15];
cz q[16], q[25];
cz q[3], q[31];
cz q[33], q[1];
cz q[24], q[12];
cz q[14], q[22];
cz q[2], q[32];
cz q[23], q[13];
cz q[0], q[30];
cz q[21], q[11];
