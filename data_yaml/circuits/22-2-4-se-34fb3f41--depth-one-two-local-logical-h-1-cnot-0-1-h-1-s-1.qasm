OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[14];
s q[3];
s q[0];
s q[15];
s q[20];
s q[21];
s q[13];
s q[12];
cz q[10], q[16];
cz q[8], q[19];
cz q[6], q[4];
cz q[5], q[1];
cz q[2], q[7];
cz q[17], q[11];
cz q[9], q[18];
