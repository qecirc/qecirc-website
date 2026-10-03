OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[8];
s q[7];
s q[31];
s q[0];
s q[24];
s q[17];
s q[9];
cz q[6], q[5];
cz q[30], q[29];
cz q[23], q[22];
cz q[15], q[14];
cz q[4], q[3];
cz q[28], q[27];
cz q[21], q[20];
cz q[13], q[12];
cz q[2], q[1];
cz q[26], q[25];
cz q[19], q[18];
cz q[11], q[10];
