OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[16];
z q[13];
z q[11];
z q[9];
z q[7];
x q[19];
x q[10];
czyx q[4];
czyx q[17];
cxyz q[18];
id q[0];
cxyz q[11];
cxyz q[9];
czyx q[7];
swap q[17], q[18];
swap q[16], q[13];
swap q[9], q[7];
swap q[11], q[4];
