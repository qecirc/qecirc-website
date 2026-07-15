OPENQASM 2.0;
include "qelib1.inc";

qreg q[41];

h q[31];
h q[26];
h q[21];
h q[16];
h q[36];
h q[15];
h q[14];
h q[13];
h q[12];
h q[11];
h q[10];
h q[9];
h q[8];
h q[7];
h q[6];
h q[5];
h q[4];
h q[3];
h q[2];
h q[1];
h q[0];
barrier q;

cx q[15], q[32];
cx q[14], q[27];
cx q[13], q[22];
cx q[12], q[17];
barrier q;

cx q[31], q[32];
cx q[26], q[27];
cx q[21], q[22];
cx q[16], q[17];
cx q[36], q[37];
barrier q;

cx q[15], q[27];
cx q[14], q[22];
cx q[13], q[17];
cx q[12], q[37];
barrier q;

cx q[11], q[33];
cx q[10], q[28];
cx q[9], q[23];
cx q[8], q[18];
barrier q;

cx q[32], q[33];
cx q[27], q[28];
cx q[22], q[23];
cx q[17], q[18];
cx q[37], q[38];
barrier q;

cx q[11], q[28];
cx q[10], q[23];
cx q[9], q[18];
cx q[8], q[38];
barrier q;

cx q[7], q[34];
cx q[6], q[29];
cx q[5], q[24];
cx q[4], q[19];
barrier q;

cx q[33], q[34];
cx q[28], q[29];
cx q[23], q[24];
cx q[18], q[19];
cx q[38], q[39];
barrier q;

cx q[7], q[29];
cx q[6], q[24];
cx q[5], q[19];
cx q[4], q[39];
barrier q;

cx q[3], q[35];
cx q[2], q[30];
cx q[1], q[25];
cx q[0], q[20];
barrier q;

cx q[34], q[35];
cx q[29], q[30];
cx q[24], q[25];
cx q[19], q[20];
cx q[39], q[40];
barrier q;

cx q[3], q[30];
cx q[2], q[25];
cx q[1], q[20];
cx q[0], q[40];
barrier q;

