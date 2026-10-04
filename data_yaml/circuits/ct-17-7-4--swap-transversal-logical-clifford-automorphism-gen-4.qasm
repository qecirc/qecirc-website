OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[17];

z q[8];
z q[4];
y q[12];
z q[14];
x q[11];
x q[16];
x q[7];
y q[15];
cxyz q[13];
czyx q[6];
czyx q[3];
cxyz q[2];
cxyz q[9];
cxyz q[8];
cxyz q[12];
czyx q[14];
czyx q[15];
swap q[16], q[7];
swap q[6], q[11];
swap q[9], q[15];
swap q[12], q[14];
swap q[5], q[16];
swap q[8], q[3];
swap q[13], q[6];
swap q[1], q[9];
swap q[4], q[12];
swap q[10], q[8];
