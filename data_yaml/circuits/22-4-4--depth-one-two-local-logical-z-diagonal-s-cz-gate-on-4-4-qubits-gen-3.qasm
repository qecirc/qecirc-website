OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

s q[6];
s q[4];
s q[2];
s q[14];
s q[12];
s q[1];
s q[0];
s q[13];
s q[11];
s q[3];
s q[5];
s q[7];
id q[20];
cz q[6], q[11];
cz q[4], q[14];
cz q[2], q[0];
cz q[12], q[7];
cz q[1], q[3];
cz q[13], q[5];
