OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[9];

cxyz q[6];
cxyz q[5];
czyx q[4];
cxyz q[8];
id q[0];
swap q[5], q[8];
swap q[6], q[5];
