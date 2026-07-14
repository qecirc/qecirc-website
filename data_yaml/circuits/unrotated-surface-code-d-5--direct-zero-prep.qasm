OPENQASM 2.0;
include "qelib1.inc";

qreg q[41];

h q[26];
h q[27];
h q[28];
h q[29];
h q[30];
h q[21];
h q[22];
h q[23];
h q[24];
h q[25];
h q[16];
h q[17];
h q[18];
h q[19];
h q[20];
h q[36];
h q[37];
h q[38];
h q[39];
h q[40];
barrier q;

cx q[26], q[15];
cx q[27], q[11];
cx q[28], q[7];
cx q[29], q[3];
barrier q;

cx q[26], q[31];
cx q[27], q[32];
cx q[28], q[33];
cx q[29], q[34];
cx q[30], q[35];
barrier q;

cx q[27], q[15];
cx q[28], q[11];
cx q[29], q[7];
cx q[30], q[3];
barrier q;

cx q[21], q[14];
cx q[22], q[10];
cx q[23], q[6];
cx q[24], q[2];
barrier q;

cx q[21], q[26];
cx q[22], q[27];
cx q[23], q[28];
cx q[24], q[29];
cx q[25], q[30];
barrier q;

cx q[22], q[14];
cx q[23], q[10];
cx q[24], q[6];
cx q[25], q[2];
barrier q;

cx q[16], q[13];
cx q[17], q[9];
cx q[18], q[5];
cx q[19], q[1];
barrier q;

cx q[16], q[21];
cx q[17], q[22];
cx q[18], q[23];
cx q[19], q[24];
cx q[20], q[25];
barrier q;

cx q[17], q[13];
cx q[18], q[9];
cx q[19], q[5];
cx q[20], q[1];
barrier q;

cx q[36], q[12];
cx q[37], q[8];
cx q[38], q[4];
cx q[39], q[0];
barrier q;

cx q[36], q[16];
cx q[37], q[17];
cx q[38], q[18];
cx q[39], q[19];
cx q[40], q[20];
barrier q;

cx q[37], q[12];
cx q[38], q[8];
cx q[39], q[4];
cx q[40], q[0];
barrier q;

