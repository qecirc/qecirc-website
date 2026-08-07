OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[0];
s q[1];
s q[2];
s q[3];
s q[10];
s q[7];
s q[6];
s q[13];
s q[17];
s q[12];
s q[8];
s q[9];
s q[11];
s q[19];
id q[14];
cz q[0], q[12];
cz q[1], q[9];
cz q[2], q[10];
cz q[3], q[6];
cz q[7], q[17];
cz q[13], q[8];
cz q[11], q[19];
