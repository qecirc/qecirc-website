OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[8];
s q[7];
s q[31];
s q[2];
s q[26];
s q[19];
s q[11];
s q[1];
s q[25];
s q[18];
s q[10];
s q[0];
s q[24];
s q[17];
s q[9];
cz q[6], q[4];
cz q[30], q[28];
cz q[23], q[21];
cz q[15], q[13];
cz q[5], q[3];
cz q[29], q[27];
cz q[22], q[20];
cz q[14], q[12];
