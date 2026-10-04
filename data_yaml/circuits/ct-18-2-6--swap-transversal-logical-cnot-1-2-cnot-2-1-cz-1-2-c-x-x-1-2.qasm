OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[14];
z q[12];
z q[11];
z q[8];
z q[7];
z q[5];
z q[2];
x q[15];
z q[17];
czyx q[16];
czyx q[9];
cxyz q[6];
cxyz q[4];
cxyz q[3];
id q[0];
czyx q[12];
czyx q[8];
cxyz q[7];
cxyz q[5];
czyx q[2];
czyx q[15];
swap q[9], q[6];
swap q[4], q[2];
swap q[5], q[17];
swap q[8], q[3];
swap q[13], q[7];
swap q[14], q[9];
swap q[10], q[2];
swap q[11], q[8];
swap q[12], q[17];
swap q[16], q[7];
