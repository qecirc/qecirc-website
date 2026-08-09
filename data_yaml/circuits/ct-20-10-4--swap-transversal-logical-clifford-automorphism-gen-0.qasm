OPENQASM 2.0;
include "qelib1.inc";

qreg q[19];

z q[15];
z q[7];
z q[2];
z q[16];
swap q[14], q[18];
swap q[0], q[9];
swap q[5], q[11];
swap q[1], q[8];
swap q[3], q[17];
swap q[4], q[13];
swap q[12], q[10];
swap q[2], q[16];
swap q[15], q[7];
