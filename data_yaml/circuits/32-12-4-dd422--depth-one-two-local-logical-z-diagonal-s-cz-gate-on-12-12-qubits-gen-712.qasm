OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[22];
s q[14];
s q[21];
s q[13];
s q[20];
s q[12];
s q[18];
s q[10];
cz q[16], q[30];
cz q[8], q[6];
cz q[7], q[23];
cz q[31], q[15];
cz q[5], q[29];
cz q[4], q[28];
cz q[3], q[27];
cz q[2], q[24];
cz q[26], q[0];
cz q[19], q[17];
cz q[11], q[9];
cz q[1], q[25];
