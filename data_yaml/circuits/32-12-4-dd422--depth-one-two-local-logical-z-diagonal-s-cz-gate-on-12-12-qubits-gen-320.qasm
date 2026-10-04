OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[8];
s q[31];
s q[29];
s q[14];
s q[28];
s q[13];
s q[26];
s q[11];
s q[25];
s q[10];
s q[24];
s q[9];
cz q[16], q[7];
cz q[6], q[20];
cz q[30], q[27];
cz q[23], q[3];
cz q[15], q[12];
cz q[5], q[22];
cz q[4], q[21];
cz q[2], q[19];
cz q[1], q[18];
cz q[0], q[17];
