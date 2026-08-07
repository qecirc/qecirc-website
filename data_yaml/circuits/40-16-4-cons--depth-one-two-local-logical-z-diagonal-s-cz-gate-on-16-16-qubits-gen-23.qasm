OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

cz q[12], q[35];
cz q[10], q[36];
cz q[9], q[37];
cz q[8], q[38];
cz q[7], q[39];
cz q[6], q[11];
cz q[5], q[29];
cz q[4], q[32];
cz q[3], q[33];
cz q[2], q[34];
cz q[1], q[22];
cz q[31], q[20];
cz q[28], q[18];
cz q[26], q[16];
cz q[24], q[14];
cz q[0], q[21];
cz q[30], q[19];
cz q[27], q[17];
cz q[25], q[15];
cz q[23], q[13];
