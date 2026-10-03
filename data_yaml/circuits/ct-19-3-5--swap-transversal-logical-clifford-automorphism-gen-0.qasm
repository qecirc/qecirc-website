OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

cxyz q[13];
czyx q[12];
cxyz q[11];
czyx q[9];
czyx q[7];
cxyz q[5];
czyx q[4];
cxyz q[18];
swap q[15], q[16];
id q[0];
swap q[7], q[18];
swap q[11], q[4];
swap q[12], q[5];
swap q[13], q[9];
