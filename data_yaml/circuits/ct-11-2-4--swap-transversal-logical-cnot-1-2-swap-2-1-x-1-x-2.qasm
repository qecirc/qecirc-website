OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[11];

z q[9];
z q[5];
z q[3];
z q[1];
y q[6];
czyx q[8];
czyx q[4];
czyx q[10];
cxyz q[2];
cxyz q[7];
id q[0];
czyx q[9];
czyx q[5];
czyx q[3];
cxyz q[1];
cxyz q[6];
swap q[7], q[1];
swap q[3], q[10];
swap q[2], q[1];
swap q[4], q[10];
