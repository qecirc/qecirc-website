OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[8];
s q[7];
s q[31];
s q[6];
s q[30];
s q[23];
s q[15];
s q[5];
s q[29];
s q[22];
s q[14];
s q[0];
s q[24];
s q[17];
s q[9];
cz q[4], q[2];
cz q[28], q[26];
cz q[21], q[19];
cz q[13], q[11];
cz q[3], q[1];
cz q[27], q[25];
cz q[20], q[18];
cz q[12], q[10];
