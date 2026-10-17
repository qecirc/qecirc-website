OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[5];
s q[29];
s q[4];
s q[28];
s q[3];
s q[27];
s q[2];
s q[26];
cz q[16], q[6];
cz q[8], q[30];
cz q[7], q[15];
cz q[31], q[23];
cz q[22], q[14];
cz q[21], q[13];
cz q[20], q[12];
cz q[19], q[11];
cz q[1], q[0];
cz q[25], q[24];
cz q[18], q[9];
cz q[10], q[17];
