OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

z q[4];
y q[12];
z q[10];
y q[7];
y q[11];
y q[5];
czyx q[8];
czyx q[6];
cxyz q[9];
cxyz q[2];
id q[0];
czyx q[12];
cxyz q[7];
czyx q[11];
cxyz q[5];
swap q[11], q[5];
swap q[2], q[12];
swap q[7], q[5];
swap q[10], q[11];
swap q[9], q[2];
swap q[6], q[12];
swap q[3], q[9];
swap q[8], q[5];
