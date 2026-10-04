OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

s q[6];
s q[4];
s q[3];
s q[15];
s q[1];
s q[11];
s q[9];
s q[5];
s q[7];
s q[17];
s q[16];
s q[2];
id q[12];
cz q[6], q[1];
cz q[4], q[5];
cz q[3], q[9];
cz q[15], q[16];
cz q[11], q[17];
cz q[7], q[2];
