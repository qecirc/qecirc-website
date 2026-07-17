OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[10];
z q[8];
z q[6];
z q[4];
y q[14];
y q[17];
y q[11];
y q[13];
y q[19];
x q[9];
y q[16];
x q[18];
czyx q[3];
swap q[15], q[12];
id q[0];
cxyz q[10];
cxyz q[8];
czyx q[6];
czyx q[17];
czyx q[19];
cxyz q[16];
cxyz q[18];
swap q[7], q[9];
swap q[19], q[16];
swap q[17], q[18];
swap q[8], q[6];
swap q[10], q[3];
