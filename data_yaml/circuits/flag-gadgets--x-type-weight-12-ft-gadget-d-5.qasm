OPENQASM 2.0;
include "qelib1.inc";

qreg q[15];
creg rec[3];

h q[0];
cx q[0], q[14];
cx q[0], q[13];
cx q[14], q[9];
cx q[0], q[11];
cx q[14], q[8];
cx q[13], q[5];
cx q[0], q[10];
cx q[13], q[4];
cx q[0], q[12];
cx q[0], q[7];
cx q[0], q[6];
cx q[0], q[14];
cx q[0], q[3];
measure q[14] -> rec[0];
cx q[0], q[2];
cx q[0], q[13];
cx q[0], q[1];
measure q[13] -> rec[1];
cx q[0], q[12];
measure q[12] -> rec[2];
