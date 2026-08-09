OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[31];
s q[6];
s q[15];
s q[5];
s q[14];
s q[4];
s q[13];
s q[3];
s q[12];
s q[2];
s q[11];
s q[1];
s q[10];
s q[0];
s q[9];
cz q[8], q[7];
cz q[30], q[23];
cz q[29], q[22];
cz q[28], q[21];
cz q[27], q[20];
cz q[26], q[19];
cz q[25], q[18];
cz q[24], q[17];
