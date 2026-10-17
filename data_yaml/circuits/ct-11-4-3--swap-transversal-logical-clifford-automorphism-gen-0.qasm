OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

x q[10];
x q[4];
x q[7];
cxyz q[8];
czyx q[5];
czyx q[2];
cxyz q[9];
czyx q[6];
sx q[0];
cxyz q[10];
czyx q[4];
cxyz q[7];
swap q[8], q[6];
swap q[9], q[4];
swap q[2], q[7];
swap q[5], q[10];
