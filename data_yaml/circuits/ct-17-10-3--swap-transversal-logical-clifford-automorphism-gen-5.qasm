OPENQASM 2.0;
include "qelib1.inc";

qreg q[17];

z q[9];
z q[6];
z q[2];
z q[14];
swap q[15], q[5];
swap q[10], q[8];
swap q[16], q[4];
swap q[11], q[7];
id q[0];
swap q[1], q[14];
swap q[2], q[13];
