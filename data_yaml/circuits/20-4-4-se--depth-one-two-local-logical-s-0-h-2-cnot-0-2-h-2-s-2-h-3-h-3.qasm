OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[12];
s q[6];
s q[4];
s q[17];
s q[3];
s q[15];
s q[1];
s q[16];
s q[14];
s q[5];
s q[13];
s q[19];
s q[18];
s q[7];
id q[8];
cz q[12], q[16];
cz q[6], q[4];
cz q[17], q[14];
cz q[3], q[5];
cz q[15], q[18];
cz q[1], q[7];
cz q[13], q[19];
