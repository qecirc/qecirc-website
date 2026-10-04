OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[7];
s q[6];
s q[5];
s q[4];
s q[3];
s q[2];
s q[1];
s q[8];
s q[21];
s q[9];
s q[18];
s q[19];
s q[16];
s q[11];
id q[12];
cz q[7], q[2];
cz q[6], q[19];
cz q[5], q[3];
cz q[4], q[16];
cz q[1], q[8];
cz q[21], q[11];
cz q[9], q[18];
