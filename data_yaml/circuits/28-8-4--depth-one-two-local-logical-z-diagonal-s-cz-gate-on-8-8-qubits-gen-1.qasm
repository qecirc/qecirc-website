OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

s q[24];
s q[5];
s q[13];
s q[1];
s q[0];
s q[19];
s q[27];
s q[26];
s q[20];
s q[25];
cz q[14], q[12];
cz q[10], q[9];
cz q[7], q[23];
cz q[4], q[2];
cz q[3], q[17];
cz q[8], q[21];
cz q[11], q[16];
cz q[18], q[6];
cz q[15], q[22];
