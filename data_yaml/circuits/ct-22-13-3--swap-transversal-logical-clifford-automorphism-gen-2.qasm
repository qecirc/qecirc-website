OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

z q[12];
z q[8];
z q[4];
z q[3];
x q[20];
czyx q[16];
czyx q[14];
czyx q[2];
czyx q[19];
cxyz q[9];
czyx q[17];
cxyz q[5];
cxyz q[6];
id q[0];
cxyz q[8];
cxyz q[3];
swap q[9], q[17];
swap q[19], q[6];
swap q[16], q[5];
swap q[12], q[10];
swap q[3], q[14];
swap q[8], q[2];
