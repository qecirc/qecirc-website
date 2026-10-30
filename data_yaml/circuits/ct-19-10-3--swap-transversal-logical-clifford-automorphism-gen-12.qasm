OPENQASM 2.0;
include "qelib1.inc";
gate cxyz q0 { U(pi/2, 0, pi/2) q0; }
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[19];

z q[11];
z q[5];
z q[14];
czyx q[13];
czyx q[18];
cxyz q[3];
czyx q[17];
cxyz q[15];
cxyz q[9];
czyx q[16];
cxyz q[7];
id q[0];
cxyz q[11];
czyx q[5];
swap q[15], q[9];
swap q[17], q[16];
swap q[12], q[7];
swap q[18], q[3];
swap q[13], q[17];
swap q[14], q[3];
swap q[5], q[7];
swap q[11], q[9];
