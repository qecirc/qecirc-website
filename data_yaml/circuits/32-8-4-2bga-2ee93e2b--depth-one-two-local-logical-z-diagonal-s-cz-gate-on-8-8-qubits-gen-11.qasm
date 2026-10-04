OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[24], q[22];
cz q[19], q[2];
cz q[16], q[9];
cz q[13], q[4];
cz q[10], q[14];
cz q[8], q[5];
cz q[26], q[20];
cz q[21], q[0];
cz q[6], q[15];
cz q[3], q[23];
cz q[1], q[30];
cz q[7], q[28];
cz q[25], q[31];
cz q[17], q[12];
cz q[11], q[18];
cz q[27], q[29];
