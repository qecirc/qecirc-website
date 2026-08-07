OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[12];
s q[5];
s q[1];
s q[10];
s q[9];
s q[13];
s q[21];
s q[14];
s q[15];
s q[20];
cz q[16], q[18];
cz q[8], q[11];
cz q[6], q[2];
cz q[3], q[7];
cz q[0], q[4];
cz q[17], q[19];
