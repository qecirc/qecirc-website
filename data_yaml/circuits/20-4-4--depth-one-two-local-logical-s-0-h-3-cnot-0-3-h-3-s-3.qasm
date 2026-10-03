OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[10];
s q[7];
s q[5];
s q[3];
s q[2];
s q[16];
s q[0];
s q[13];
s q[15];
s q[6];
s q[8];
s q[18];
s q[19];
s q[12];
id q[11];
cz q[10], q[13];
cz q[7], q[5];
cz q[3], q[0];
cz q[2], q[18];
cz q[16], q[6];
cz q[15], q[12];
cz q[8], q[19];
