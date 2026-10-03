OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[5];
z q[2];
z q[11];
x q[10];
x q[9];
z q[14];
x q[12];
z q[6];
y q[13];
y q[7];
x q[4];
czyx q[8];
cxyz q[1];
cxyz q[15];
czyx q[0];
czyx q[3];
czyx q[11];
czyx q[10];
czyx q[9];
cxyz q[6];
cxyz q[13];
czyx q[4];
swap q[1], q[3];
swap q[6], q[13];
swap q[0], q[9];
swap q[10], q[4];
swap q[5], q[3];
swap q[15], q[6];
swap q[11], q[10];
swap q[8], q[0];
