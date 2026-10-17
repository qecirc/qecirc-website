OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[11];
z q[7];
z q[5];
z q[3];
y q[8];
czyx q[10];
czyx q[6];
czyx q[12];
cxyz q[4];
cxyz q[9];
id q[0];
czyx q[11];
czyx q[7];
czyx q[5];
cxyz q[3];
cxyz q[8];
swap q[9], q[3];
swap q[5], q[12];
swap q[4], q[3];
swap q[6], q[12];
