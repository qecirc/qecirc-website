OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[9];
s q[8];
s q[7];
s q[10];
s q[3];
s q[27];
s q[35];
s q[29];
cz q[28], q[26];
cz q[22], q[34];
cz q[21], q[1];
cz q[39], q[33];
cz q[15], q[31];
cz q[12], q[4];
cz q[11], q[38];
cz q[20], q[23];
cz q[6], q[16];
cz q[25], q[0];
cz q[37], q[19];
cz q[30], q[13];
cz q[5], q[17];
cz q[32], q[14];
cz q[24], q[2];
cz q[36], q[18];
