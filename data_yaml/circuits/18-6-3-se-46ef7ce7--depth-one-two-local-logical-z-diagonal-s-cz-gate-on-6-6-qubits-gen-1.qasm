OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[0];
s q[14];
s q[12];
s q[5];
s q[13];
s q[15];
cz q[10], q[17];
cz q[8], q[7];
cz q[6], q[9];
cz q[3], q[1];
cz q[16], q[11];
cz q[4], q[2];
