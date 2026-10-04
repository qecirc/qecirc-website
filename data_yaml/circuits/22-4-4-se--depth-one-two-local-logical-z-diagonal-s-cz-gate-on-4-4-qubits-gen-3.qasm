OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[12];
s q[5];
s q[2];
s q[4];
s q[9];
s q[13];
s q[21];
s q[14];
s q[18];
s q[15];
cz q[16], q[1];
cz q[8], q[17];
cz q[6], q[20];
cz q[3], q[11];
cz q[0], q[10];
cz q[7], q[19];
