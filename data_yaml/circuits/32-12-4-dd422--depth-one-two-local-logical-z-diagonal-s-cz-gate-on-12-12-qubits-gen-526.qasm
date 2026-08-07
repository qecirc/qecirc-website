OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[8];
s q[4];
s q[28];
s q[3];
s q[27];
s q[0];
s q[24];
cz q[7], q[31];
cz q[6], q[5];
cz q[30], q[29];
cz q[23], q[14];
cz q[15], q[22];
cz q[21], q[13];
cz q[20], q[12];
cz q[2], q[1];
cz q[26], q[25];
cz q[19], q[10];
cz q[11], q[18];
cz q[17], q[9];
