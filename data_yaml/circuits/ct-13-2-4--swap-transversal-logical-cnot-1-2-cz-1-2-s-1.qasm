OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[13];

czyx q[10];
cxyz q[7];
cxyz q[5];
czyx q[12];
czyx q[9];
cxyz q[3];
swap q[6], q[4];
id q[0];
swap q[12], q[3];
swap q[5], q[9];
swap q[10], q[7];
