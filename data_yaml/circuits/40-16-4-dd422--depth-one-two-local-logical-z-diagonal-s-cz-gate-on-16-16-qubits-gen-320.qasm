OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[7];
s q[18];
s q[5];
s q[16];
s q[1];
s q[12];
s q[0];
s q[11];
cz q[20], q[8];
cz q[10], q[29];
cz q[9], q[38];
cz q[39], q[19];
cz q[37], q[28];
cz q[6], q[4];
cz q[36], q[25];
cz q[27], q[34];
cz q[17], q[15];
cz q[35], q[26];
cz q[3], q[2];
cz q[33], q[23];
cz q[24], q[32];
cz q[14], q[13];
cz q[31], q[22];
cz q[30], q[21];
