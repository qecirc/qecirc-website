OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[15];

z q[8];
x q[11];
z q[3];
z q[2];
x q[13];
swap q[6], q[9];
swap q[14], q[10];
id q[0];
cxyz q[8];
swap q[2], q[6];
swap q[7], q[14];
swap q[4], q[11];
swap q[5], q[11];
