OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[20];

z q[6];
z q[5];
z q[11];
y q[9];
y q[13];
czyx q[14];
czyx q[8];
cxyz q[7];
cxyz q[3];
czyx q[18];
cxyz q[19];
id q[0];
czyx q[11];
cxyz q[9];
swap q[12], q[13];
swap q[6], q[4];
swap q[7], q[18];
swap q[8], q[3];
swap q[11], q[19];
swap q[14], q[9];
