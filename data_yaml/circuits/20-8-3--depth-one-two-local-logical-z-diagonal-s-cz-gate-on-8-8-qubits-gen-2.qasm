OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[2];
s q[1];
s q[0];
s q[11];
s q[3];
s q[8];
s q[9];
s q[10];
cz q[12], q[13];
cz q[6], q[7];
cz q[4], q[5];
cz q[16], q[17];
cz q[14], q[15];
cz q[19], q[18];
