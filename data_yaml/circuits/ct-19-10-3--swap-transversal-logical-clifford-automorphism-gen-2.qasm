OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[11];
z q[5];
z q[14];
cxyz q[8];
czyx q[13];
cxyz q[18];
czyx q[17];
czyx q[15];
cxyz q[9];
cxyz q[16];
czyx q[10];
id q[0];
swap q[15], q[9];
swap q[17], q[16];
swap q[18], q[10];
swap q[14], q[3];
swap q[8], q[13];
swap q[11], q[6];
