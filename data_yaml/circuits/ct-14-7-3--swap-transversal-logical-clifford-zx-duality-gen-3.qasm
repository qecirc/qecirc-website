OPENQASM 2.0;
include "qelib1.inc";

qreg q[14];

z q[11];
z q[2];
y q[13];
z q[9];
x q[12];
h q[7];
h q[4];
h q[3];
h q[10];
h q[6];
h q[1];
h q[5];
h q[8];
id q[0];
h q[11];
h q[2];
h q[13];
h q[9];
h q[12];
swap q[1], q[8];
swap q[3], q[6];
swap q[11], q[2];
swap q[10], q[13];
swap q[4], q[9];
