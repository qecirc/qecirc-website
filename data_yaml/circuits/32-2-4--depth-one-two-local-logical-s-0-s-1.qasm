OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[22];
s q[8];
s q[7];
s q[26];
s q[0];
s q[16];
s q[19];
s q[27];
cz q[28], q[5];
cz q[25], q[23];
cz q[20], q[9];
cz q[15], q[4];
cz q[12], q[21];
cz q[6], q[29];
cz q[2], q[11];
cz q[1], q[24];
cz q[3], q[10];
cz q[18], q[17];
cz q[13], q[30];
cz q[14], q[31];
