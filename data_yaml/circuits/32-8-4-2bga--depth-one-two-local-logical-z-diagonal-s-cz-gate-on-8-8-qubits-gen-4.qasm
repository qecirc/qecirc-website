OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[24], q[21];
cz q[16], q[31];
cz q[13], q[20];
cz q[10], q[23];
cz q[9], q[19];
cz q[8], q[12];
cz q[7], q[15];
cz q[6], q[30];
cz q[4], q[3];
cz q[2], q[27];
cz q[1], q[26];
cz q[0], q[5];
cz q[11], q[22];
cz q[14], q[28];
cz q[17], q[29];
cz q[25], q[18];
