OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[20];
s q[39];
s q[8];
s q[19];
s q[5];
s q[16];
s q[2];
s q[13];
cz q[10], q[9];
cz q[38], q[29];
cz q[7], q[6];
cz q[37], q[27];
cz q[28], q[36];
cz q[18], q[17];
cz q[35], q[26];
cz q[4], q[3];
cz q[34], q[24];
cz q[25], q[33];
cz q[15], q[14];
cz q[32], q[23];
cz q[1], q[0];
cz q[31], q[21];
cz q[22], q[30];
cz q[12], q[11];
