OPENQASM 2.0;
include "qelib1.inc";

qreg q[36];

cz q[24], q[20];
cz q[14], q[21];
cz q[12], q[34];
cz q[11], q[4];
cz q[10], q[8];
cz q[9], q[15];
cz q[7], q[35];
cz q[6], q[23];
cz q[5], q[30];
cz q[3], q[2];
cz q[1], q[25];
cz q[0], q[18];
cz q[26], q[28];
cz q[32], q[17];
cz q[22], q[16];
cz q[19], q[27];
cz q[31], q[29];
cz q[33], q[13];
