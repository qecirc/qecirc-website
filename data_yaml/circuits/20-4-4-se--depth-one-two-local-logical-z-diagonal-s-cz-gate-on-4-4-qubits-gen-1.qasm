OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[2];
s q[15];
s q[11];
s q[18];
cz q[12], q[0];
cz q[10], q[1];
cz q[6], q[14];
cz q[4], q[7];
cz q[17], q[8];
cz q[3], q[9];
cz q[16], q[13];
cz q[5], q[19];
