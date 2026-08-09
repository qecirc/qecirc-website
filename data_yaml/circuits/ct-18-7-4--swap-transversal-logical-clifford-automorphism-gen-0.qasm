OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[14];
z q[11];
z q[15];
y q[16];
czyx q[4];
czyx q[13];
cxyz q[10];
cxyz q[12];
id q[0];
czyx q[11];
cxyz q[16];
swap q[13], q[10];
swap q[4], q[12];
swap q[14], q[15];
swap q[11], q[16];
