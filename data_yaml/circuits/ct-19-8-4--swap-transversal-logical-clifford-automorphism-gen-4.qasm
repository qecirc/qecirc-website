OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[11];
z q[6];
z q[2];
x q[13];
z q[12];
y q[18];
y q[8];
y q[15];
cxyz q[9];
czyx q[7];
czyx q[5];
swap q[4], q[10];
id q[0];
cxyz q[2];
cxyz q[13];
czyx q[12];
czyx q[8];
cxyz q[15];
swap q[6], q[18];
swap q[9], q[7];
swap q[8], q[15];
swap q[13], q[12];
swap q[5], q[2];
