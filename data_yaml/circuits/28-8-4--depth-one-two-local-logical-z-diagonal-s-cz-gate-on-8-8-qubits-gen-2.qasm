OPENQASM 2.0;
include "qelib1.inc";

qreg q[28];

s q[24];
s q[14];
s q[3];
s q[9];
s q[1];
s q[0];
s q[19];
s q[27];
s q[26];
s q[25];
cz q[10], q[4];
cz q[7], q[17];
cz q[5], q[8];
cz q[2], q[21];
cz q[13], q[6];
cz q[11], q[22];
cz q[18], q[23];
cz q[16], q[12];
cz q[15], q[20];
