OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[5];
s q[4];
s q[3];
s q[7];
s q[0];
s q[15];
s q[20];
s q[13];
cz q[14], q[6];
cz q[10], q[16];
cz q[8], q[9];
cz q[2], q[21];
cz q[1], q[12];
cz q[17], q[19];
cz q[11], q[18];
