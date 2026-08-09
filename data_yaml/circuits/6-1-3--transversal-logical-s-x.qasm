OPENQASM 2.0;
include "qelib1.inc";
gate czyx q0 { U(pi/2, pi/2, pi/2) q0; }

qreg q[6];

czyx q[3];
czyx q[2];
czyx q[1];
czyx q[4];
czyx q[5];
id q[0];
