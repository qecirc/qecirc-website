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
cz q[5], q[2];
cz q[29], q[26];
cz q[22], q[19];
cz q[14], q[11];
cz q[4], q[0];
cz q[28], q[24];
cz q[21], q[17];
cz q[13], q[9];
cz q[3], q[1];
cz q[27], q[25];
cz q[20], q[18];
cz q[12], q[10];
