OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }

qreg q[9];

cxyz q[6];
cxyz q[5];
cxyz q[4];
cxyz q[7];
cxyz q[8];
id q[0];
