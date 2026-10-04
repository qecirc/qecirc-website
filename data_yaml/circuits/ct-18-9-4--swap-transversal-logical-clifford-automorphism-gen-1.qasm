OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[8];
z q[6];
z q[3];
z q[2];
z q[13];
x q[14];
x q[10];
x q[7];
z q[11];
czyx q[4];
cxyz q[1];
cxyz q[16];
cxyz q[17];
swap q[12], q[5];
id q[0];
cxyz q[8];
czyx q[6];
czyx q[14];
czyx q[7];
swap q[10], q[11];
swap q[2], q[9];
swap q[3], q[13];
swap q[4], q[17];
swap q[16], q[7];
swap q[6], q[1];
swap q[8], q[14];
