OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

cz q[12], q[20];
cz q[10], q[22];
cz q[9], q[18];
cz q[8], q[16];
cz q[7], q[14];
cz q[6], q[31];
cz q[5], q[1];
cz q[4], q[28];
cz q[3], q[26];
cz q[2], q[24];
cz q[0], q[19];
cz q[30], q[21];
cz q[27], q[17];
cz q[25], q[15];
cz q[23], q[13];
cz q[11], q[36];
cz q[29], q[35];
cz q[32], q[37];
cz q[33], q[38];
cz q[34], q[39];
