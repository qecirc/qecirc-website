OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[16];

z q[2];
y q[15];
z q[13];
y q[4];
cxyz q[9];
czyx q[6];
czyx q[3];
cxyz q[12];
swap q[10], q[8];
swap q[11], q[7];
id q[0];
swap q[1], q[13];
swap q[2], q[14];
swap q[6], q[12];
swap q[9], q[3];
