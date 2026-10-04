OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

cxyz q[12];
czyx q[11];
cxyz q[10];
czyx q[8];
czyx q[6];
cxyz q[4];
czyx q[3];
cxyz q[17];
swap q[14], q[15];
id q[0];
swap q[6], q[17];
swap q[10], q[3];
swap q[11], q[4];
swap q[12], q[8];
