OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg rec[3];

h q[7];
h q[8];
h q[9];
cx q[9], q[0];
cx q[8], q[0];
cx q[7], q[0];
cx q[5], q[8];
cx q[6], q[0];
cx q[4], q[8];
cx q[9], q[0];
cx q[3], q[0];
h q[9];
cx q[2], q[0];
measure q[9] -> rec[0];
cx q[8], q[0];
cx q[1], q[0];
h q[8];
cx q[7], q[0];
measure q[8] -> rec[1];
h q[7];
measure q[7] -> rec[2];
