OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[10];
s q[6];
s q[4];
s q[3];
s q[8];
s q[7];
s q[12];
s q[11];
s q[9];
s q[13];
s q[15];
s q[16];
id q[21];
cz q[10], q[6];
cz q[4], q[15];
cz q[3], q[16];
cz q[8], q[7];
cz q[12], q[11];
cz q[9], q[13];
