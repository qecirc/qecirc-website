OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[16];
s q[8];
s q[6];
s q[3];
s q[2];
s q[1];
s q[0];
s q[15];
s q[10];
s q[5];
s q[17];
s q[9];
s q[11];
s q[14];
id q[12];
cz q[16], q[17];
cz q[8], q[14];
cz q[6], q[11];
cz q[3], q[9];
cz q[2], q[0];
cz q[1], q[15];
cz q[10], q[5];
