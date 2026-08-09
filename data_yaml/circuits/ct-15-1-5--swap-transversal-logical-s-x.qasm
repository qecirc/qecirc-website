OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[13];
z q[10];
z q[9];
z q[7];
y q[8];
czyx q[12];
czyx q[11];
czyx q[14];
cxyz q[6];
cxyz q[5];
cxyz q[4];
id q[0];
czyx q[13];
czyx q[10];
czyx q[9];
cxyz q[7];
cxyz q[8];
swap q[6], q[5];
swap q[7], q[5];
swap q[9], q[14];
swap q[10], q[14];
