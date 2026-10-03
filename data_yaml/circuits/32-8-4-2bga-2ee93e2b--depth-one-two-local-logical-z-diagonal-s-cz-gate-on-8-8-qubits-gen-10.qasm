OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[6];
s q[4];
s q[3];
s q[2];
s q[1];
s q[0];
s q[7];
s q[5];
s q[12];
s q[28];
s q[31];
s q[30];
s q[29];
s q[23];
s q[18];
s q[15];
cz q[24], q[22];
cz q[19], q[25];
cz q[16], q[20];
cz q[13], q[17];
cz q[10], q[14];
cz q[8], q[11];
cz q[26], q[9];
cz q[21], q[27];
