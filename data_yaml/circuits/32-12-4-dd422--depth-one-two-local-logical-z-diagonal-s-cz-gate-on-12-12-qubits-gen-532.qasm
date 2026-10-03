OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[8];
s q[31];
s q[28];
s q[13];
s q[27];
s q[12];
s q[24];
s q[9];
cz q[16], q[7];
cz q[6], q[22];
cz q[30], q[29];
cz q[23], q[5];
cz q[15], q[14];
cz q[4], q[21];
cz q[3], q[20];
cz q[2], q[18];
cz q[26], q[25];
cz q[19], q[1];
cz q[11], q[10];
cz q[0], q[17];
