OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[14];
s q[10];
s q[8];
s q[6];
s q[3];
s q[2];
s q[1];
s q[21];
s q[18];
s q[9];
s q[11];
s q[13];
s q[16];
s q[12];
id q[17];
cz q[14], q[2];
cz q[10], q[18];
cz q[8], q[1];
cz q[6], q[11];
cz q[3], q[13];
cz q[21], q[9];
cz q[16], q[12];
