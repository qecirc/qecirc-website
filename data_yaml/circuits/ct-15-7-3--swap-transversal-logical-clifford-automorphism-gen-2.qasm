OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[3];
z q[14];
h q[8];
h q[5];
h q[4];
h q[11];
h q[12];
sx q[7];
sx q[10];
s q[2];
s q[6];
s q[13];
s q[9];
id q[0];
sx q[3];
sx q[14];
swap q[6], q[9];
swap q[5], q[12];
swap q[3], q[7];
