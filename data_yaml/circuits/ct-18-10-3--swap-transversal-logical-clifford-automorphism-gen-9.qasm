OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

x q[12];
x q[17];
z q[15];
z q[6];
cxyz q[10];
cxyz q[4];
czyx q[3];
cxyz q[2];
czyx q[16];
czyx q[8];
cxyz q[9];
id q[0];
cxyz q[17];
cxyz q[15];
swap q[8], q[5];
swap q[2], q[9];
swap q[3], q[11];
swap q[16], q[15];
swap q[17], q[9];
swap q[4], q[3];
swap q[10], q[8];
swap q[7], q[16];
