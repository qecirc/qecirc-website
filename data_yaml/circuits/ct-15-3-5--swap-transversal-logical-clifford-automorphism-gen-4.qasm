OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

z q[9];
z q[8];
z q[3];
z q[1];
z q[14];
z q[12];
y q[10];
cxyz q[7];
cxyz q[6];
czyx q[5];
cxyz q[4];
czyx q[0];
czyx q[8];
czyx q[3];
cxyz q[14];
czyx q[12];
cxyz q[10];
swap q[6], q[5];
swap q[7], q[0];
swap q[1], q[10];
swap q[2], q[14];
swap q[4], q[12];
swap q[9], q[6];
swap q[13], q[7];
swap q[3], q[2];
swap q[8], q[1];
swap q[11], q[12];
