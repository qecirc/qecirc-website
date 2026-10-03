OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

s q[10];
s q[7];
s q[41];
s q[28];
s q[40];
s q[27];
s q[39];
s q[26];
s q[38];
s q[25];
s q[37];
s q[44];
id q[47];
cz q[10], q[7];
cz q[41], q[28];
cz q[40], q[27];
cz q[39], q[26];
cz q[38], q[25];
cz q[37], q[44];
