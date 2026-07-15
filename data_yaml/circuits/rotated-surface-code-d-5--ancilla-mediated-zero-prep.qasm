OPENQASM 2.0;
include "qelib1.inc";

qreg q[49];

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
cx q[5], q[28];
cx q[22], q[38];
cx q[11], q[47];
barrier q;

cx q[28], q[15];
cx q[38], q[12];
cx q[47], q[14];
barrier q;

cx q[28], q[16];
cx q[38], q[13];
barrier q;

cx q[28], q[7];
cx q[38], q[6];
barrier q;

cx q[5], q[28];
cx q[22], q[38];
cx q[11], q[47];
barrier q;

cx q[3], q[43];
cx q[4], q[33];
cx q[8], q[25];
barrier q;

cx q[43], q[11];
cx q[33], q[22];
cx q[25], q[5];
barrier q;

cx q[43], q[6];
cx q[33], q[7];
barrier q;

cx q[43], q[23];
cx q[33], q[9];
barrier q;

cx q[3], q[43];
cx q[4], q[33];
cx q[8], q[25];
barrier q;

cx q[2], q[30];
cx q[10], q[40];
cx q[24], q[48];
barrier q;

cx q[30], q[8];
cx q[40], q[4];
cx q[48], q[3];
barrier q;

cx q[30], q[9];
cx q[40], q[23];
barrier q;

cx q[30], q[1];
cx q[40], q[0];
barrier q;

cx q[2], q[30];
cx q[10], q[40];
cx q[24], q[48];
barrier q;

cx q[17], q[45];
cx q[20], q[35];
cx q[21], q[26];
barrier q;

cx q[45], q[24];
cx q[35], q[10];
cx q[26], q[2];
barrier q;

cx q[45], q[0];
cx q[35], q[1];
barrier q;

cx q[45], q[18];
cx q[35], q[19];
barrier q;

cx q[17], q[45];
cx q[20], q[35];
cx q[21], q[26];
barrier q;

