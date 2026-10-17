OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[21];

cxyz q[8];
czyx q[16];
cxyz q[3];
czyx q[14];
czyx q[1];
czyx q[4];
cxyz q[15];
czyx q[17];
cxyz q[20];
cxyz q[18];
swap q[11], q[13];
id q[7];
swap q[15], q[17];
swap q[4], q[18];
swap q[3], q[14];
swap q[16], q[20];
swap q[8], q[1];
