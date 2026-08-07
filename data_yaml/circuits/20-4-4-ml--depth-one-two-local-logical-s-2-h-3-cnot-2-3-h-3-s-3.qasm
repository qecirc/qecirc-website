OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[8];
s q[4];
s q[2];
s q[1];
s q[0];
s q[7];
s q[11];
s q[9];
s q[14];
s q[15];
s q[17];
s q[18];
s q[19];
s q[13];
id q[16];
cz q[8], q[19];
cz q[4], q[1];
cz q[2], q[18];
cz q[0], q[11];
cz q[7], q[13];
cz q[9], q[15];
cz q[14], q[17];
