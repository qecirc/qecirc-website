OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[4];
x q[13];
x q[18];
z q[3];
z q[17];
y q[15];
x q[16];
czyx q[11];
czyx q[14];
czyx q[9];
cxyz q[6];
cxyz q[10];
id q[0];
cxyz q[13];
czyx q[18];
cxyz q[3];
cxyz q[15];
czyx q[16];
swap q[9], q[6];
swap q[14], q[10];
swap q[8], q[17];
swap q[18], q[3];
swap q[13], q[16];
swap q[11], q[15];
