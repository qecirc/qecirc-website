OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[14];

z q[7];
z q[2];
x q[12];
z q[1];
x q[11];
z q[0];
x q[10];
z q[3];
x q[13];
z q[9];
x q[6];
z q[8];
x q[5];
cxyz q[4];
cxyz q[7];
cxyz q[2];
cxyz q[12];
cxyz q[1];
cxyz q[11];
cxyz q[0];
cxyz q[10];
cxyz q[3];
cxyz q[13];
cxyz q[9];
cxyz q[6];
cxyz q[8];
cxyz q[5];
