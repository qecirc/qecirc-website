OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[10];
z q[4];
z q[17];
x q[16];
y q[14];
cxyz q[13];
czyx q[3];
cxyz q[12];
czyx q[2];
cxyz q[11];
cxyz q[8];
cxyz q[5];
czyx q[15];
cxyz q[9];
id q[0];
czyx q[4];
czyx q[16];
czyx q[14];
swap q[15], q[9];
swap q[12], q[2];
swap q[3], q[8];
swap q[7], q[17];
swap q[10], q[6];
swap q[11], q[14];
swap q[13], q[16];
swap q[4], q[5];
