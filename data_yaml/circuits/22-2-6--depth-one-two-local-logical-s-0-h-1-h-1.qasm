OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

s q[10];
s q[7];
s q[5];
s q[4];
s q[3];
s q[1];
s q[17];
s q[18];
s q[12];
s q[11];
s q[16];
s q[19];
s q[15];
s q[20];
id q[9];
cz q[10], q[16];
cz q[7], q[11];
cz q[5], q[17];
cz q[4], q[18];
cz q[3], q[1];
cz q[12], q[19];
cz q[15], q[20];
