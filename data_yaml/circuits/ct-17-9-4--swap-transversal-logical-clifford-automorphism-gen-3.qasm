OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[7];
z q[4];
z q[2];
z q[15];
z q[12];
z q[13];
x q[9];
x q[6];
x q[16];
y q[10];
y q[14];
cxyz q[11];
czyx q[5];
czyx q[1];
czyx q[4];
czyx q[2];
cxyz q[15];
cxyz q[12];
czyx q[13];
cxyz q[9];
cxyz q[6];
czyx q[16];
cxyz q[14];
swap q[0], q[10];
swap q[7], q[8];
swap q[11], q[5];
swap q[6], q[16];
swap q[13], q[9];
swap q[1], q[15];
swap q[2], q[14];
swap q[4], q[12];
