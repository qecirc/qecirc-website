OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

cz q[11], q[14];
cz q[6], q[15];
cz q[4], q[16];
cz q[3], q[2];
cz q[10], q[0];
cz q[13], q[1];
cz q[12], q[8];
cz q[5], q[9];
cz q[17], q[7];
