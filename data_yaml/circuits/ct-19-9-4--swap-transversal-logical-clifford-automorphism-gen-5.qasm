OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[13];
z q[9];
z q[7];
z q[6];
z q[4];
z q[3];
z q[2];
x q[10];
z q[15];
y q[8];
z q[18];
z q[12];
z q[16];
czyx q[11];
id q[0];
cxyz q[13];
czyx q[9];
czyx q[6];
cxyz q[3];
cxyz q[2];
czyx q[10];
cxyz q[8];
swap q[18], q[16];
swap q[4], q[17];
swap q[3], q[10];
swap q[6], q[2];
swap q[9], q[8];
swap q[13], q[11];
