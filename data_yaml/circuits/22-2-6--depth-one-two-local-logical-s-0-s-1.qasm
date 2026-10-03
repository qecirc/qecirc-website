OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[7];
s q[6];
s q[2];
s q[1];
s q[0];
s q[8];
s q[20];
s q[21];
cz q[14], q[11];
cz q[10], q[12];
cz q[5], q[19];
cz q[4], q[18];
cz q[3], q[9];
cz q[17], q[16];
cz q[13], q[15];
