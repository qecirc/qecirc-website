OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[5];
z q[2];
z q[1];
y q[15];
z q[0];
y q[12];
cxyz q[11];
cxyz q[10];
cxyz q[9];
cxyz q[6];
czyx q[13];
cxyz q[7];
czyx q[4];
swap q[8], q[14];
czyx q[2];
czyx q[1];
cxyz q[15];
czyx q[0];
czyx q[12];
swap q[6], q[13];
swap q[11], q[4];
swap q[5], q[3];
swap q[0], q[9];
swap q[10], q[12];
swap q[1], q[7];
swap q[2], q[15];
