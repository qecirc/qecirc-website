OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[10];
s q[4];
s q[0];
s q[8];
s q[7];
s q[13];
s q[12];
s q[11];
cz q[18], q[5];
cz q[14], q[2];
cz q[6], q[16];
cz q[3], q[1];
cz q[9], q[20];
cz q[17], q[21];
cz q[19], q[15];
