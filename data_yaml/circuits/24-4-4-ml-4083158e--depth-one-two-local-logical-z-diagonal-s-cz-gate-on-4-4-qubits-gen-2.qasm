OPENQASM 2.0;
include "qelib1.inc";

qreg q[24];

s q[6];
s q[4];
s q[7];
s q[21];
s q[2];
s q[14];
s q[18];
s q[19];
s q[17];
s q[11];
s q[22];
s q[23];
id q[10];
cz q[6], q[17];
cz q[4], q[14];
cz q[7], q[22];
cz q[21], q[11];
cz q[2], q[18];
cz q[19], q[23];
