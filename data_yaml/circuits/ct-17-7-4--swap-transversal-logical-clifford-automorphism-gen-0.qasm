OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[13];
z q[10];
z q[14];
y q[15];
czyx q[3];
czyx q[12];
cxyz q[9];
cxyz q[11];
czyx q[10];
cxyz q[15];
swap q[12], q[9];
swap q[3], q[11];
swap q[13], q[14];
swap q[10], q[15];
