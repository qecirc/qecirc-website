OPENQASM 2.0;
include "qelib1.inc";

qreg q[23];

s q[7];
s q[6];
s q[8];
s q[4];
s q[3];
s q[5];
s q[12];
s q[22];
s q[16];
s q[17];
s q[11];
s q[21];
cz q[7], q[16];
cz q[6], q[12];
cz q[8], q[22];
cz q[4], q[17];
cz q[3], q[11];
cz q[5], q[21];
