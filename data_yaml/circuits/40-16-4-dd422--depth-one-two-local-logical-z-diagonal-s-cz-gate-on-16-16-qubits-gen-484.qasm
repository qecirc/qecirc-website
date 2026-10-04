OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[7];
s q[18];
s q[4];
s q[15];
s q[3];
s q[14];
s q[2];
s q[13];
cz q[20], q[8];
cz q[10], q[29];
cz q[9], q[38];
cz q[39], q[19];
cz q[37], q[28];
cz q[6], q[5];
cz q[36], q[26];
cz q[27], q[35];
cz q[17], q[16];
cz q[34], q[25];
cz q[33], q[24];
cz q[32], q[23];
cz q[1], q[0];
cz q[31], q[21];
cz q[22], q[30];
cz q[12], q[11];
