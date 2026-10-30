OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[8];
z q[5];
z q[3];
z q[16];
y q[9];
z q[14];
z q[10];
x q[17];
czyx q[6];
czyx q[4];
cxyz q[1];
czyx q[7];
id q[0];
cxyz q[8];
cxyz q[16];
czyx q[14];
cxyz q[17];
swap q[13], q[9];
swap q[1], q[7];
swap q[3], q[2];
swap q[5], q[11];
swap q[12], q[10];
swap q[14], q[17];
swap q[6], q[16];
swap q[8], q[4];
