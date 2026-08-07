OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[16];
s q[7];
s q[4];
s q[3];
s q[1];
s q[0];
s q[17];
s q[13];
s q[19];
s q[11];
s q[8];
s q[6];
s q[18];
s q[14];
cz q[16], q[11];
cz q[7], q[3];
cz q[4], q[17];
cz q[1], q[19];
cz q[0], q[18];
cz q[13], q[14];
cz q[8], q[6];
