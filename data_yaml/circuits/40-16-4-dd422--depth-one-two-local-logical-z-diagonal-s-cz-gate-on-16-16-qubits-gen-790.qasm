OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

cz q[20], q[38];
cz q[10], q[8];
cz q[9], q[19];
cz q[39], q[29];
cz q[7], q[35];
cz q[37], q[5];
cz q[28], q[16];
cz q[18], q[26];
cz q[6], q[36];
cz q[27], q[17];
cz q[4], q[34];
cz q[25], q[15];
cz q[3], q[31];
cz q[33], q[1];
cz q[24], q[12];
cz q[14], q[22];
cz q[2], q[32];
cz q[23], q[13];
cz q[0], q[30];
cz q[21], q[11];
