OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[18];

z q[15];
z q[12];
z q[16];
y q[17];
czyx q[5];
czyx q[14];
cxyz q[11];
cxyz q[13];
id q[0];
czyx q[12];
cxyz q[17];
swap q[14], q[11];
swap q[5], q[13];
swap q[15], q[16];
swap q[12], q[17];
