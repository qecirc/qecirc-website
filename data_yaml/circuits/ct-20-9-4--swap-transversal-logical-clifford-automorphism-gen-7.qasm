OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[10];
z q[8];
z q[6];
z q[4];
x q[18];
z q[11];
z q[12];
y q[9];
z q[19];
z q[13];
x q[17];
czyx q[14];
czyx q[7];
cxyz q[5];
cxyz q[15];
czyx q[16];
id q[0];
czyx q[8];
cxyz q[4];
czyx q[18];
cxyz q[11];
cxyz q[9];
cxyz q[19];
czyx q[17];
swap q[12], q[13];
swap q[15], q[16];
swap q[6], q[3];
swap q[18], q[11];
swap q[5], q[17];
swap q[7], q[19];
swap q[8], q[4];
swap q[14], q[9];
