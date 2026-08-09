OPENQASM 2.0;
include "qelib1.inc";

qreg q[22];

s q[12];
s q[2];
s q[1];
s q[0];
s q[9];
s q[15];
s q[14];
s q[18];
s q[13];
s q[20];
cz q[16], q[6];
cz q[8], q[3];
cz q[4], q[19];
cz q[11], q[7];
cz q[10], q[17];
cz q[5], q[21];
