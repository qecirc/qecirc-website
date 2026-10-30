OPENQASM 2.0;
include "qelib1.inc";

qreg q[40];

s q[7];
s q[6];
s q[24];
s q[22];
s q[23];
s q[21];
s q[34];
s q[35];
id q[39];
cz q[7], q[6];
cz q[24], q[22];
cz q[23], q[21];
cz q[34], q[35];
