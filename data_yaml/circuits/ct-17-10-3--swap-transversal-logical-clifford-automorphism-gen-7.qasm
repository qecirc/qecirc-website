OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[3];
x q[11];
y q[16];
x q[10];
x q[15];
z q[14];
czyx q[9];
czyx q[6];
czyx q[2];
czyx q[1];
czyx q[13];
czyx q[8];
id q[0];
cxyz q[3];
cxyz q[11];
czyx q[10];
czyx q[14];
swap q[2], q[8];
swap q[7], q[14];
swap q[1], q[10];
swap q[11], q[13];
swap q[6], q[2];
swap q[12], q[13];
swap q[3], q[14];
swap q[9], q[1];
