OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[14];

z q[7];
x q[10];
z q[6];
z q[5];
x q[12];
swap q[13], q[9];
id q[0];
cxyz q[7];
swap q[5], q[8];
swap q[2], q[9];
swap q[10], q[11];
swap q[1], q[5];
swap q[3], q[10];
