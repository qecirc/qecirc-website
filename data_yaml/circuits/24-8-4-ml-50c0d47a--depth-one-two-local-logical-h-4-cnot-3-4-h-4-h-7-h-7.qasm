OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[1];
s q[8];
s q[15];
s q[14];
s q[12];
s q[11];
s q[17];
s q[19];
id q[21];
cz q[1], q[8];
cz q[15], q[12];
cz q[14], q[11];
cz q[17], q[19];
