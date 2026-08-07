OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[6];
s q[30];
s q[4];
s q[28];
s q[3];
s q[27];
s q[2];
s q[26];
s q[1];
s q[25];
s q[0];
s q[24];
cz q[16], q[5];
cz q[8], q[29];
cz q[7], q[14];
cz q[31], q[22];
cz q[23], q[15];
cz q[21], q[13];
cz q[20], q[12];
cz q[19], q[11];
cz q[18], q[10];
cz q[17], q[9];
