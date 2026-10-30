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
s q[1];
s q[25];
s q[18];
s q[10];
s q[0];
s q[24];
s q[17];
s q[9];
cz q[5], q[3];
cz q[29], q[27];
cz q[22], q[20];
cz q[14], q[12];
cz q[4], q[2];
cz q[28], q[26];
cz q[21], q[19];
cz q[13], q[11];
