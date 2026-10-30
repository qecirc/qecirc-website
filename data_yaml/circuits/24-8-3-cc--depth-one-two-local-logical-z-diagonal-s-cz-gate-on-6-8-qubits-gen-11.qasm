OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[14];
s q[9];
s q[19];
s q[7];
s q[6];
s q[8];
s q[18];
s q[10];
s q[20];
s q[17];
s q[11];
s q[21];
cz q[14], q[10];
cz q[9], q[20];
cz q[19], q[18];
cz q[7], q[17];
cz q[6], q[11];
cz q[8], q[21];
