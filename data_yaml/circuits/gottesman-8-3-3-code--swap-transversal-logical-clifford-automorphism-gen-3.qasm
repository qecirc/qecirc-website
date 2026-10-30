OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[8];

z q[4];
y q[2];
z q[6];
y q[3];
cxyz q[0];
cxyz q[1];
cxyz q[7];
cxyz q[5];
cxyz q[4];
cxyz q[2];
cxyz q[6];
cxyz q[3];
swap q[5], q[2];
swap q[7], q[3];
swap q[4], q[3];
swap q[1], q[2];
