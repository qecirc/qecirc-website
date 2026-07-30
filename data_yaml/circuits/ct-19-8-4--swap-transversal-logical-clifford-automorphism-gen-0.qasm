OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[14];
z q[11];
z q[16];
y q[17];
czyx q[6];
czyx q[4];
czyx q[13];
cxyz q[10];
cxyz q[12];
cxyz q[15];
swap q[18], q[8];
id q[0];
czyx q[11];
cxyz q[17];
swap q[13], q[10];
swap q[4], q[12];
swap q[6], q[15];
swap q[14], q[16];
swap q[11], q[17];
