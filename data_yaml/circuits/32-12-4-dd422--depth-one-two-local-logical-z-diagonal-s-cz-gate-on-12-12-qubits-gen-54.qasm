OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[8];
s q[6];
s q[30];
s q[5];
s q[29];
s q[4];
s q[28];
s q[1];
s q[25];
s q[0];
s q[24];
cz q[7], q[31];
cz q[23], q[15];
cz q[22], q[14];
cz q[21], q[13];
cz q[3], q[2];
cz q[27], q[26];
cz q[20], q[11];
cz q[12], q[19];
cz q[18], q[10];
cz q[17], q[9];
