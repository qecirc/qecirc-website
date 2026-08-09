OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[18];
s q[10];
s q[8];
s q[5];
s q[3];
s q[2];
s q[0];
s q[20];
s q[21];
s q[9];
s q[19];
s q[11];
s q[12];
s q[13];
id q[17];
cz q[18], q[2];
cz q[10], q[9];
cz q[8], q[0];
cz q[5], q[13];
cz q[3], q[20];
cz q[21], q[12];
cz q[19], q[11];
