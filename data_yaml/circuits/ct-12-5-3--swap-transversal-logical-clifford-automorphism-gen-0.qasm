OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[12];

z q[2];
x q[11];
cxyz q[5];
czyx q[8];
czyx q[9];
cxyz q[4];
swap q[7], q[10];
id q[0];
cxyz q[2];
czyx q[11];
swap q[9], q[4];
swap q[5], q[8];
swap q[2], q[11];
