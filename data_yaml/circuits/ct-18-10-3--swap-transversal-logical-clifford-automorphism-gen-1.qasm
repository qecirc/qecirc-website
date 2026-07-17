OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

z q[10];
z q[7];
z q[3];
z q[15];
swap q[16], q[6];
swap q[11], q[9];
swap q[17], q[5];
swap q[12], q[8];
id q[0];
swap q[2], q[15];
swap q[3], q[14];
