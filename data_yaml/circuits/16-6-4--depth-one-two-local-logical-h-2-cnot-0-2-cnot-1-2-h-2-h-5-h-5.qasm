OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];

s q[8];
s q[4];
s q[0];
s q[15];
s q[12];
s q[3];
s q[7];
s q[11];
id q[14];
cz q[8], q[0];
cz q[4], q[12];
cz q[15], q[7];
cz q[3], q[11];
