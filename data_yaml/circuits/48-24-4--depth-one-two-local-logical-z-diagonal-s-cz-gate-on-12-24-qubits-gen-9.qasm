OPENQASM 2.0;
include "qelib1.inc";

qreg q[48];

s q[12];
s q[7];
s q[3];
s q[28];
s q[2];
s q[27];
s q[1];
s q[26];
s q[0];
s q[25];
s q[11];
s q[44];
id q[47];
cz q[12], q[7];
cz q[3], q[28];
cz q[2], q[27];
cz q[1], q[26];
cz q[0], q[25];
cz q[11], q[44];
