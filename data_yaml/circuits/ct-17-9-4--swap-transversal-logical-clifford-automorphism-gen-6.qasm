OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[11];
z q[7];
z q[5];
z q[4];
z q[3];
z q[2];
y q[15];
x q[12];
cxyz q[8];
cxyz q[13];
cxyz q[9];
cxyz q[6];
czyx q[16];
czyx q[10];
swap q[0], q[14];
cxyz q[5];
czyx q[4];
cxyz q[3];
czyx q[15];
czyx q[12];
swap q[13], q[9];
swap q[8], q[16];
swap q[1], q[14];
swap q[12], q[10];
swap q[3], q[15];
swap q[5], q[9];
swap q[11], q[16];
swap q[4], q[10];
swap q[7], q[15];
