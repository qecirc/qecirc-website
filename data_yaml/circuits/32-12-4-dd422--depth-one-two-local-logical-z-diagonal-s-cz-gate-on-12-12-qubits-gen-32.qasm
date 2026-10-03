OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[8];
s q[31];
s q[30];
s q[15];
s q[29];
s q[14];
s q[28];
s q[13];
s q[27];
s q[12];
s q[26];
s q[11];
cz q[16], q[7];
cz q[6], q[23];
cz q[5], q[22];
cz q[4], q[21];
cz q[3], q[20];
cz q[2], q[19];
cz q[1], q[17];
cz q[25], q[24];
cz q[18], q[0];
cz q[10], q[9];
