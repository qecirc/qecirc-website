OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[8];
s q[6];
s q[5];
s q[4];
s q[3];
s q[19];
s q[16];
s q[9];
s q[13];
s q[12];
s q[15];
s q[11];
id q[14];
cz q[8], q[11];
cz q[6], q[15];
cz q[5], q[9];
cz q[4], q[16];
cz q[3], q[13];
cz q[19], q[12];
