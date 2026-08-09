OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[5];
s q[14];
s q[4];
s q[13];
s q[3];
s q[12];
s q[2];
s q[11];
cz q[16], q[6];
cz q[8], q[23];
cz q[7], q[30];
cz q[31], q[15];
cz q[29], q[22];
cz q[28], q[21];
cz q[27], q[20];
cz q[26], q[19];
cz q[1], q[0];
cz q[25], q[17];
cz q[18], q[24];
cz q[10], q[9];
