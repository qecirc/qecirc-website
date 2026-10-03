OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[11];
x q[14];
x q[13];
y q[18];
z q[3];
z q[12];
x q[15];
x q[16];
z q[7];
czyx q[8];
cxyz q[5];
cxyz q[17];
czyx q[9];
cxyz q[6];
czyx q[10];
id q[0];
czyx q[11];
czyx q[13];
cxyz q[18];
czyx q[3];
czyx q[12];
cxyz q[15];
cxyz q[16];
cxyz q[7];
swap q[17], q[9];
swap q[14], q[4];
swap q[10], q[7];
swap q[18], q[12];
swap q[13], q[6];
swap q[5], q[3];
swap q[8], q[15];
swap q[11], q[16];
