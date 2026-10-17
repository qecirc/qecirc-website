OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

s q[12];
s q[6];
s q[3];
s q[24];
s q[2];
s q[23];
s q[1];
s q[22];
s q[0];
s q[21];
s q[11];
s q[45];
id q[47];
cz q[12], q[6];
cz q[3], q[24];
cz q[2], q[23];
cz q[1], q[22];
cz q[0], q[21];
cz q[11], q[45];
