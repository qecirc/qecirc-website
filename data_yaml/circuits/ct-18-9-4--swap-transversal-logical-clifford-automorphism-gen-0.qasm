OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[12];
z q[8];
z q[4];
z q[1];
x q[16];
z q[13];
y q[9];
x q[17];
x q[15];
cxyz q[5];
czyx q[7];
czyx q[11];
swap q[3], q[2];
id q[0];
czyx q[8];
cxyz q[4];
cxyz q[1];
cxyz q[16];
czyx q[9];
swap q[6], q[13];
swap q[16], q[9];
swap q[1], q[7];
swap q[4], q[11];
swap q[8], q[5];
