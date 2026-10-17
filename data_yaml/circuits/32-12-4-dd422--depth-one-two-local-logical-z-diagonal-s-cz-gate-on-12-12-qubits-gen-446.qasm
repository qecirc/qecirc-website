OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[6];
s q[30];
s q[23];
s q[15];
s q[3];
s q[27];
s q[20];
s q[12];
cz q[16], q[0];
cz q[8], q[24];
cz q[7], q[17];
cz q[31], q[9];
cz q[5], q[1];
cz q[29], q[25];
cz q[22], q[18];
cz q[14], q[10];
cz q[4], q[2];
cz q[28], q[26];
cz q[21], q[19];
cz q[13], q[11];
