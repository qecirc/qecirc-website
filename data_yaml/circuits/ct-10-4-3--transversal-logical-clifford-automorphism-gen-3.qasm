OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[10];

z q[7];
z q[4];
z q[0];
x q[3];
z q[5];
cxyz q[2];
cxyz q[1];
cxyz q[8];
cxyz q[9];
cxyz q[6];
cxyz q[7];
cxyz q[4];
cxyz q[0];
cxyz q[3];
cxyz q[5];
