OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[16];
z q[9];
z q[8];
z q[5];
z q[15];
y q[17];
y q[12];
x q[14];
x q[19];
y q[10];
x q[18];
cxyz q[11];
czyx q[7];
cxyz q[4];
id q[0];
czyx q[9];
cxyz q[15];
czyx q[14];
swap q[6], q[12];
swap q[7], q[4];
swap q[15], q[14];
swap q[11], q[9];
