OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[8];
z q[6];
z q[4];
z q[11];
z q[2];
z q[1];
czyx q[12];
swap q[10], q[7];
id q[0];
cxyz q[8];
czyx q[4];
cxyz q[11];
swap q[2], q[1];
swap q[12], q[11];
swap q[8], q[4];
