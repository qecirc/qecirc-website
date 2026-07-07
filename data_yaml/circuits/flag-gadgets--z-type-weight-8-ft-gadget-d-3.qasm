OPENQASM 2.0;
include "qelib1.inc";

qreg q[9];
creg rec[1];

h q[8];
cx q[8], q[0];
cx q[7], q[0];
cx q[6], q[0];
cx q[5], q[0];
cx q[4], q[0];
cx q[3], q[0];
cx q[2], q[0];
cx q[1], q[0];
cx q[8], q[0];
h q[8];
measure q[8] -> rec[0];
