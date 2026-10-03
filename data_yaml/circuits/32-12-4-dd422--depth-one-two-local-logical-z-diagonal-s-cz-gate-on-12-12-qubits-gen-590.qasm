OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[7];
s q[31];
s q[23];
s q[15];
s q[20];
s q[12];
s q[19];
s q[11];
cz q[16], q[8];
cz q[6], q[30];
cz q[5], q[28];
cz q[29], q[4];
cz q[22], q[21];
cz q[14], q[13];
cz q[3], q[27];
cz q[2], q[26];
cz q[1], q[24];
cz q[25], q[0];
cz q[18], q[17];
cz q[10], q[9];
