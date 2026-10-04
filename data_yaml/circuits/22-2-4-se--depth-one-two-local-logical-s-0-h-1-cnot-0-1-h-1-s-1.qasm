OPENQASM 2.0;
include "qelib1.inc";

qreg q[21];

s q[12];
s q[8];
s q[6];
s q[5];
s q[0];
s q[4];
s q[9];
s q[13];
s q[16];
s q[17];
s q[14];
s q[15];
id q[20];
cz q[12], q[5];
cz q[8], q[14];
cz q[6], q[13];
cz q[0], q[4];
cz q[9], q[15];
cz q[16], q[17];
