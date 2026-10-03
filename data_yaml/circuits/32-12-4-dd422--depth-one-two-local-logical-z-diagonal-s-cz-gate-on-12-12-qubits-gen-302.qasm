OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[31];
s q[0];
s q[9];
cz q[8], q[7];
cz q[6], q[1];
cz q[30], q[18];
cz q[23], q[25];
cz q[15], q[10];
cz q[5], q[2];
cz q[29], q[19];
cz q[22], q[26];
cz q[14], q[11];
cz q[4], q[3];
cz q[28], q[20];
cz q[21], q[27];
cz q[13], q[12];
cz q[24], q[17];
