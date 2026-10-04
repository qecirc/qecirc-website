OPENQASM 2.0;
include "qelib1.inc";

qreg q[30];

s q[8];
s q[7];
s q[6];
s q[25];
s q[10];
s q[26];
s q[29];
s q[28];
id q[21];
cz q[8], q[28];
cz q[7], q[25];
cz q[6], q[26];
cz q[10], q[29];
