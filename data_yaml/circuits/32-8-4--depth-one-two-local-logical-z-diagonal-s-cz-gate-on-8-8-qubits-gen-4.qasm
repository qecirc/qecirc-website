OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

cz q[24], q[4];
cz q[18], q[5];
cz q[12], q[26];
cz q[9], q[22];
cz q[8], q[1];
cz q[7], q[15];
cz q[6], q[16];
cz q[3], q[30];
cz q[2], q[0];
cz q[31], q[23];
cz q[25], q[17];
cz q[13], q[27];
cz q[10], q[21];
cz q[19], q[29];
cz q[11], q[28];
cz q[14], q[20];
