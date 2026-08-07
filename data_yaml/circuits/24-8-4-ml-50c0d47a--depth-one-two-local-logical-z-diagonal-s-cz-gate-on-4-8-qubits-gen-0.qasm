OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[6];
s q[4];
s q[3];
s q[15];
s q[14];
s q[12];
s q[11];
s q[9];
id q[21];
cz q[6], q[14];
cz q[4], q[12];
cz q[3], q[11];
cz q[15], q[9];
