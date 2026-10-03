OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[15];

czyx q[3];
czyx q[7];
czyx q[14];
czyx q[10];
cxyz q[2];
cxyz q[6];
cxyz q[13];
cxyz q[9];
id q[0];
swap q[10], q[2];
swap q[14], q[13];
swap q[7], q[9];
swap q[3], q[6];
