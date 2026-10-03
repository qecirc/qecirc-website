OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[27];
s q[12];
s q[26];
s q[11];
s q[25];
s q[10];
s q[24];
s q[9];
cz q[16], q[21];
cz q[8], q[28];
cz q[7], q[4];
cz q[31], q[13];
cz q[6], q[22];
cz q[30], q[29];
cz q[23], q[5];
cz q[15], q[14];
cz q[3], q[20];
cz q[2], q[19];
cz q[1], q[18];
cz q[0], q[17];
