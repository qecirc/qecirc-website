OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[12];
z q[11];
z q[6];
z q[4];
z q[17];
z q[15];
y q[13];
cxyz q[10];
cxyz q[9];
czyx q[8];
cxyz q[7];
czyx q[3];
id q[0];
czyx q[11];
czyx q[6];
cxyz q[17];
czyx q[15];
cxyz q[13];
swap q[9], q[8];
swap q[10], q[3];
swap q[4], q[13];
swap q[5], q[17];
swap q[7], q[15];
swap q[12], q[9];
swap q[16], q[10];
swap q[6], q[5];
swap q[11], q[4];
swap q[14], q[15];
