OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[9];
z q[3];
z q[2];
x q[11];
x q[16];
z q[8];
cxyz q[6];
czyx q[12];
cxyz q[1];
cxyz q[10];
czyx q[15];
cxyz q[13];
czyx q[7];
czyx q[4];
cxyz q[14];
czyx q[5];
id q[0];
cxyz q[9];
cxyz q[2];
czyx q[11];
czyx q[16];
swap q[4], q[14];
swap q[15], q[13];
swap q[1], q[5];
swap q[12], q[10];
swap q[3], q[8];
swap q[6], q[7];
swap q[2], q[16];
swap q[9], q[11];
