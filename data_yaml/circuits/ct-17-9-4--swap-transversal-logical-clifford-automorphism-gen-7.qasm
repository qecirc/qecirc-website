OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[5];
z q[4];
z q[3];
z q[2];
x q[15];
x q[13];
x q[9];
y q[10];
z q[14];
czyx q[11];
czyx q[7];
czyx q[1];
cxyz q[0];
czyx q[12];
czyx q[16];
cxyz q[4];
cxyz q[3];
cxyz q[15];
cxyz q[13];
cxyz q[9];
czyx q[10];
swap q[16], q[10];
swap q[9], q[14];
swap q[8], q[13];
swap q[6], q[16];
swap q[12], q[8];
swap q[15], q[9];
swap q[0], q[10];
swap q[1], q[14];
swap q[3], q[0];
swap q[4], q[8];
swap q[7], q[9];
swap q[11], q[4];
