OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[5];
s q[29];
s q[22];
s q[14];
s q[4];
s q[28];
s q[21];
s q[13];
s q[3];
s q[27];
s q[20];
s q[12];
s q[0];
s q[24];
s q[17];
s q[9];
cz q[16], q[6];
cz q[8], q[30];
cz q[7], q[23];
cz q[31], q[15];
cz q[2], q[1];
cz q[26], q[25];
cz q[19], q[18];
cz q[11], q[10];
