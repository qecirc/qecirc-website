OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg rec[1];

h q[4];
cx q[4], q[0];
cx q[3], q[0];
cx q[2], q[0];
cx q[1], q[0];
cx q[4], q[0];
h q[4];
measure q[4] -> rec[0];
