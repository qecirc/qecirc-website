OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[7];

z q[3];
z q[0];
z q[4];
cxyz q[1];
cxyz q[5];
cxyz q[2];
cxyz q[6];
cxyz q[3];
cxyz q[0];
cxyz q[4];
swap q[2], q[6];
swap q[5], q[2];
swap q[0], q[4];
swap q[3], q[0];
