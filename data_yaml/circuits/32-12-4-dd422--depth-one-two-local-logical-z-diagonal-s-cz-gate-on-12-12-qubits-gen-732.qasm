OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[31];
s q[5];
s q[14];
s q[1];
s q[10];
s q[0];
s q[9];
cz q[8], q[7];
cz q[6], q[4];
cz q[30], q[21];
cz q[23], q[28];
cz q[15], q[13];
cz q[29], q[22];
cz q[3], q[2];
cz q[27], q[19];
cz q[20], q[26];
cz q[12], q[11];
cz q[25], q[18];
cz q[24], q[17];
