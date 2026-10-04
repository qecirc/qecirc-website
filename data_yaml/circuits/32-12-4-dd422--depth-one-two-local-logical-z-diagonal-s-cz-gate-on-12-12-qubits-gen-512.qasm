OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[31];
s q[6];
s q[15];
s q[5];
s q[14];
s q[3];
s q[12];
cz q[8], q[7];
cz q[30], q[23];
cz q[29], q[22];
cz q[4], q[0];
cz q[28], q[17];
cz q[21], q[24];
cz q[13], q[9];
cz q[27], q[20];
cz q[2], q[1];
cz q[26], q[18];
cz q[19], q[25];
cz q[11], q[10];
