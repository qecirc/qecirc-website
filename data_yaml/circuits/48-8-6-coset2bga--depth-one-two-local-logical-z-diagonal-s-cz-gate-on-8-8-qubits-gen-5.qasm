OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

cz q[26], q[20];
cz q[19], q[31];
cz q[18], q[29];
cz q[16], q[30];
cz q[15], q[42];
cz q[14], q[32];
cz q[13], q[36];
cz q[12], q[40];
cz q[11], q[37];
cz q[10], q[34];
cz q[9], q[38];
cz q[8], q[28];
cz q[7], q[25];
cz q[6], q[43];
cz q[5], q[21];
cz q[4], q[35];
cz q[3], q[45];
cz q[2], q[23];
cz q[1], q[22];
cz q[0], q[44];
cz q[27], q[39];
cz q[47], q[24];
cz q[41], q[46];
cz q[33], q[17];
