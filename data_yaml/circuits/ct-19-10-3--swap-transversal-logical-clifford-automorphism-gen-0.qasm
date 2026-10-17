OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[11];
z q[8];
z q[5];
z q[14];
z q[4];
z q[12];
z q[17];
z q[7];
czyx q[13];
czyx q[18];
czyx q[3];
cxyz q[16];
cxyz q[10];
id q[0];
cxyz q[8];
cxyz q[5];
cxyz q[14];
czyx q[4];
czyx q[12];
czyx q[17];
cxyz q[7];
swap q[3], q[10];
swap q[17], q[16];
swap q[12], q[7];
swap q[14], q[18];
swap q[5], q[4];
swap q[8], q[13];
