OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[4];
s q[2];
s q[1];
s q[0];
s q[7];
s q[9];
cz q[10], q[21];
cz q[6], q[3];
cz q[8], q[5];
cz q[12], q[18];
cz q[11], q[15];
cz q[14], q[17];
cz q[13], q[19];
cz q[16], q[20];
