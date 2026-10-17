OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[14];

y q[12];
z q[11];
z q[1];
y q[5];
x q[6];
y q[4];
cxyz q[10];
cxyz q[8];
cxyz q[7];
czyx q[3];
czyx q[0];
cxyz q[2];
czyx q[12];
cxyz q[11];
czyx q[1];
czyx q[5];
swap q[0], q[2];
swap q[13], q[4];
swap q[10], q[3];
swap q[11], q[1];
swap q[7], q[5];
swap q[8], q[12];
