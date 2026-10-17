OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];

z q[5];
z q[1];
swap q[7], q[6];
swap q[10], q[9];
swap q[11], q[14];
id q[0];
swap q[1], q[4];
swap q[13], q[9];
swap q[3], q[6];
swap q[8], q[14];
swap q[5], q[4];
