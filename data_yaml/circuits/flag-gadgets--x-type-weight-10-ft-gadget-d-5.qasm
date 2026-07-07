OPENQASM 2.0;
include "qelib1.inc";

qreg q[13];
creg rec[3];

h q[0];
cx q[0], q[12];
cx q[0], q[11];
cx q[12], q[9];
cx q[0], q[10];
cx q[12], q[8];
cx q[11], q[5];
cx q[0], q[7];
cx q[11], q[4];
cx q[0], q[6];
cx q[0], q[12];
cx q[0], q[3];
measure q[12] -> rec[0];
cx q[0], q[2];
cx q[0], q[11];
cx q[0], q[1];
measure q[11] -> rec[1];
cx q[0], q[10];
measure q[10] -> rec[2];
