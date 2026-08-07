OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[20];
s q[10];
s q[9];
s q[39];
s q[6];
s q[36];
s q[27];
s q[17];
cz q[8], q[7];
cz q[38], q[37];
cz q[29], q[28];
cz q[19], q[18];
cz q[5], q[3];
cz q[35], q[33];
cz q[26], q[24];
cz q[16], q[14];
cz q[4], q[1];
cz q[34], q[31];
cz q[25], q[22];
cz q[15], q[12];
cz q[2], q[0];
cz q[32], q[30];
cz q[23], q[21];
cz q[13], q[11];
