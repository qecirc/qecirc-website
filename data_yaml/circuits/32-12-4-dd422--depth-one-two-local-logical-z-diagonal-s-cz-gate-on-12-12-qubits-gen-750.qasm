OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[5];
s q[29];
s q[0];
s q[24];
cz q[16], q[6];
cz q[8], q[30];
cz q[7], q[15];
cz q[31], q[23];
cz q[22], q[14];
cz q[4], q[3];
cz q[28], q[27];
cz q[21], q[12];
cz q[13], q[20];
cz q[2], q[1];
cz q[26], q[25];
cz q[19], q[10];
cz q[11], q[18];
cz q[17], q[9];
