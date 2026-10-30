OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[4];
z q[3];
z q[1];
y q[12];
y q[15];
x q[9];
y q[17];
x q[7];
y q[14];
y q[16];
czyx q[13];
cxyz q[8];
cxyz q[6];
cxyz q[11];
id q[0];
czyx q[4];
czyx q[3];
czyx q[1];
czyx q[12];
cxyz q[9];
czyx q[7];
cxyz q[14];
cxyz q[16];
swap q[5], q[17];
swap q[10], q[15];
swap q[7], q[14];
swap q[12], q[9];
swap q[3], q[11];
swap q[6], q[4];
swap q[8], q[1];
swap q[13], q[16];
