OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[13];
z q[8];
z q[6];
z q[5];
z q[4];
z q[12];
y q[14];
x q[9];
x q[11];
z q[7];
cxyz q[10];
czyx q[2];
cxyz q[1];
cxyz q[16];
cxyz q[0];
czyx q[13];
czyx q[8];
cxyz q[5];
cxyz q[4];
czyx q[12];
czyx q[9];
cxyz q[11];
cxyz q[7];
swap q[16], q[7];
swap q[9], q[15];
swap q[12], q[14];
swap q[6], q[11];
swap q[8], q[3];
swap q[1], q[9];
swap q[4], q[12];
swap q[5], q[16];
swap q[10], q[8];
swap q[13], q[6];
