OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[10];

z q[8];
z q[7];
z q[3];
z q[2];
z q[6];
z q[0];
x q[5];
cxyz q[1];
cxyz q[6];
cxyz q[0];
cxyz q[5];
swap q[2], q[9];
swap q[7], q[4];
swap q[3], q[2];
swap q[8], q[4];
