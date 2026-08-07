OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[25];
s q[10];
s q[24];
s q[9];
cz q[16], q[20];
cz q[8], q[27];
cz q[7], q[3];
cz q[31], q[12];
cz q[6], q[21];
cz q[30], q[28];
cz q[23], q[4];
cz q[15], q[13];
cz q[5], q[19];
cz q[29], q[26];
cz q[22], q[2];
cz q[14], q[11];
cz q[1], q[18];
cz q[0], q[17];
