OPENQASM 2.0;
include "qelib1.inc";

qreg q[32];

s q[3];
s q[12];
s q[2];
s q[11];
s q[1];
s q[10];
s q[0];
s q[9];
cz q[16], q[5];
cz q[8], q[22];
cz q[7], q[29];
cz q[31], q[14];
cz q[6], q[4];
cz q[30], q[21];
cz q[23], q[28];
cz q[15], q[13];
cz q[27], q[20];
cz q[26], q[19];
cz q[25], q[18];
cz q[24], q[17];
