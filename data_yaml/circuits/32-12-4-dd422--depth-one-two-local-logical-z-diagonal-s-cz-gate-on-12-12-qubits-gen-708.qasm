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
cz q[16], q[6];
cz q[8], q[30];
cz q[7], q[23];
cz q[31], q[15];
cz q[3], q[2];
cz q[27], q[26];
cz q[20], q[19];
cz q[12], q[11];
cz q[1], q[0];
cz q[25], q[24];
cz q[18], q[17];
cz q[10], q[9];
