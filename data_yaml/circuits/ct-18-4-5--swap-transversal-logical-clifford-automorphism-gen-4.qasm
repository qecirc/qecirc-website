OPENQASM 2.0;
include "qelib1.inc";

qreg q[18];

z q[7];
z q[4];
swap q[17], q[9];
swap q[14], q[11];
swap q[13], q[15];
id q[0];
swap q[2], q[9];
swap q[3], q[11];
swap q[4], q[15];
swap q[5], q[9];
swap q[6], q[11];
swap q[7], q[15];
swap q[8], q[9];
swap q[10], q[11];
swap q[12], q[15];
