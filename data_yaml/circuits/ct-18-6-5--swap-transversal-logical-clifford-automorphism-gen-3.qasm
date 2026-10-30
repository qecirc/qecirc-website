OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

z q[15];
z q[9];
swap q[14], q[10];
swap q[16], q[12];
swap q[3], q[1];
swap q[4], q[2];
swap q[11], q[7];
swap q[8], q[10];
swap q[0], q[12];
swap q[5], q[1];
swap q[6], q[2];
swap q[9], q[17];
swap q[15], q[7];
swap q[13], q[17];
