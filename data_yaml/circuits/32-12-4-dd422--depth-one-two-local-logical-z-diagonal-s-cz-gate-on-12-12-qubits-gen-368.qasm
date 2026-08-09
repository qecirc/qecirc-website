OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[5];
s q[29];
s q[22];
s q[14];
s q[4];
s q[28];
s q[21];
s q[13];
s q[2];
s q[26];
s q[19];
s q[11];
s q[1];
s q[25];
s q[18];
s q[10];
cz q[16], q[0];
cz q[8], q[24];
cz q[7], q[17];
cz q[31], q[9];
cz q[6], q[3];
cz q[30], q[27];
cz q[23], q[20];
cz q[15], q[12];
