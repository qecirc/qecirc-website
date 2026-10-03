OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[11];
z q[7];
z q[3];
z q[1];
y q[15];
z q[12];
x q[9];
czyx q[4];
cxyz q[6];
czyx q[10];
swap q[8], q[13];
swap q[0], q[16];
id q[14];
czyx q[7];
czyx q[1];
cxyz q[15];
cxyz q[12];
cxyz q[9];
swap q[6], q[10];
swap q[1], q[15];
swap q[4], q[12];
swap q[7], q[9];
