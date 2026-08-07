OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[14];
s q[5];
s q[2];
s q[1];
s q[0];
s q[17];
s q[8];
s q[6];
cz q[12], q[11];
cz q[10], q[21];
cz q[7], q[15];
cz q[4], q[9];
cz q[3], q[16];
cz q[19], q[20];
cz q[18], q[13];
