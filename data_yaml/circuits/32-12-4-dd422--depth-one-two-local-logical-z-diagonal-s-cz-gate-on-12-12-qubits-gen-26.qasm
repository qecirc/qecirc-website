OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[16];
s q[8];
s q[6];
s q[30];
s q[5];
s q[29];
s q[4];
s q[28];
s q[3];
s q[27];
s q[2];
s q[26];
cz q[7], q[31];
cz q[23], q[15];
cz q[22], q[14];
cz q[21], q[13];
cz q[20], q[12];
cz q[19], q[11];
cz q[1], q[0];
cz q[25], q[24];
cz q[18], q[9];
cz q[10], q[17];
