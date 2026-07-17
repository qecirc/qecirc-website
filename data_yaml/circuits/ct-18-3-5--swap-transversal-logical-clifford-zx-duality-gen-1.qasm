OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

z q[9];
z q[5];
swap q[8], q[6];
swap q[10], q[4];
swap q[11], q[3];
swap q[12], q[17];
swap q[14], q[15];
swap q[16], q[13];
id q[0];
swap q[9], q[5];
