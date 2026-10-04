OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

s q[20];
s q[16];
s q[11];
s q[9];
s q[7];
s q[26];
s q[5];
s q[4];
s q[2];
s q[24];
s q[1];
s q[13];
s q[0];
s q[25];
cz q[15], q[27];
cz q[8], q[14];
cz q[23], q[19];
cz q[3], q[6];
cz q[21], q[17];
cz q[12], q[10];
cz q[22], q[18];
