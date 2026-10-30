OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[29];
s q[14];
s q[28];
s q[13];
s q[26];
s q[11];
s q[25];
s q[10];
cz q[16], q[17];
cz q[8], q[24];
cz q[7], q[0];
cz q[31], q[9];
cz q[6], q[20];
cz q[30], q[27];
cz q[23], q[3];
cz q[15], q[12];
cz q[5], q[22];
cz q[4], q[21];
cz q[2], q[19];
cz q[1], q[18];
