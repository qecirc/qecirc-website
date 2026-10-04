OPENQASM 2.0;
include "qelib1.inc";

qreg q[20];

swap q[11], q[12];
swap q[15], q[9];
swap q[18], q[19];
swap q[3], q[13];
swap q[4], q[17];
swap q[8], q[7];
swap q[10], q[6];
swap q[14], q[5];
id q[0];
