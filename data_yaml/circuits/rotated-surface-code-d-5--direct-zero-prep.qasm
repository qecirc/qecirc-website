OPENQASM 2.0;
include "qelib1.inc";

qreg q[25];

h q[5];
h q[22];
h q[11];
h q[3];
h q[4];
h q[8];
h q[2];
h q[10];
h q[24];
h q[17];
h q[20];
h q[21];
barrier q;

cx q[5], q[7];
cx q[22], q[6];
barrier q;

cx q[5], q[16];
cx q[22], q[13];
barrier q;

cx q[5], q[15];
cx q[22], q[12];
cx q[11], q[14];
barrier q;

cx q[3], q[23];
cx q[4], q[9];
barrier q;

cx q[3], q[6];
cx q[4], q[7];
barrier q;

cx q[3], q[11];
cx q[4], q[22];
cx q[8], q[5];
barrier q;

cx q[2], q[1];
cx q[10], q[0];
barrier q;

cx q[2], q[9];
cx q[10], q[23];
barrier q;

cx q[2], q[8];
cx q[10], q[4];
cx q[24], q[3];
barrier q;

cx q[17], q[18];
cx q[20], q[19];
barrier q;

cx q[17], q[0];
cx q[20], q[1];
barrier q;

cx q[17], q[24];
cx q[20], q[10];
cx q[21], q[2];
barrier q;

