OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[13];
z q[11];
z q[7];
z q[17];
z q[0];
y q[14];
y q[12];
z q[10];
czyx q[5];
cxyz q[4];
czyx q[2];
cxyz q[1];
cxyz q[8];
swap q[6], q[16];
czyx q[13];
cxyz q[11];
czyx q[7];
cxyz q[17];
czyx q[0];
czyx q[14];
cxyz q[12];
swap q[1], q[8];
swap q[3], q[10];
swap q[2], q[0];
swap q[4], q[12];
swap q[5], q[14];
swap q[17], q[6];
swap q[7], q[1];
swap q[11], q[3];
swap q[9], q[2];
swap q[13], q[4];
swap q[15], q[5];
