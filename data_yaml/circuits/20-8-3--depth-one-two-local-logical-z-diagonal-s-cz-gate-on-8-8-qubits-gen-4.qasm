OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

s q[12];
s q[2];
s q[1];
s q[0];
s q[11];
s q[3];
s q[13];
s q[19];
s q[8];
s q[18];
s q[9];
s q[10];
cz q[6], q[4];
cz q[16], q[14];
cz q[17], q[15];
cz q[7], q[5];
