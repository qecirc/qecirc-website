OPENQASM 2.0;
include "qelib1.inc";

qreg q[33];
creg rec[16];

reset q[17];
reset q[18];
reset q[19];
reset q[20];
reset q[21];
reset q[22];
reset q[23];
reset q[24];
reset q[25];
reset q[26];
reset q[27];
reset q[28];
reset q[29];
reset q[30];
reset q[31];
reset q[32];
barrier q;

h q[17];
h q[19];
h q[21];
h q[22];
h q[23];
h q[24];
cx q[17], q[9];
cx q[19], q[12];
cx q[21], q[15];
cx q[22], q[4];
cx q[23], q[10];
cx q[24], q[5];
barrier q;

cx q[17], q[2];
cx q[19], q[15];
cx q[21], q[3];
cx q[22], q[8];
cx q[23], q[0];
cx q[24], q[14];
barrier q;

cx q[17], q[11];
cx q[19], q[14];
cx q[21], q[4];
cx q[22], q[7];
cx q[24], q[13];
barrier q;

h q[18];
h q[20];
cx q[17], q[0];
cx q[18], q[4];
cx q[19], q[5];
cx q[20], q[14];
cx q[21], q[1];
cx q[22], q[3];
cx q[24], q[6];
h q[17];
h q[19];
h q[22];
h q[24];
barrier q;

cx q[18], q[1];
cx q[20], q[12];
cx q[21], q[9];
barrier q;

cx q[18], q[8];
cx q[20], q[16];
cx q[21], q[12];
cx q[23], q[1];
barrier q;

cx q[18], q[10];
cx q[20], q[6];
cx q[21], q[2];
cx q[23], q[9];
h q[18];
h q[20];
h q[23];
barrier q;

cx q[21], q[16];
h q[21];
barrier q;

cx q[0], q[25];
cx q[4], q[26];
cx q[12], q[29];
cx q[3], q[30];
cx q[1], q[31];
cx q[6], q[32];
barrier q;

cx q[9], q[25];
cx q[10], q[26];
cx q[6], q[28];
cx q[2], q[29];
cx q[8], q[30];
cx q[0], q[31];
cx q[13], q[32];
barrier q;

cx q[11], q[25];
cx q[1], q[26];
cx q[16], q[29];
cx q[7], q[30];
cx q[9], q[31];
cx q[5], q[32];
barrier q;

cx q[2], q[25];
cx q[8], q[26];
cx q[16], q[28];
cx q[3], q[29];
cx q[4], q[30];
cx q[10], q[31];
cx q[14], q[32];
barrier q;

cx q[12], q[28];
cx q[15], q[29];
barrier q;

cx q[15], q[27];
cx q[14], q[28];
cx q[9], q[29];
barrier q;

cx q[5], q[27];
cx q[4], q[29];
barrier q;

cx q[14], q[27];
cx q[1], q[29];
barrier q;

cx q[12], q[27];
barrier q;

measure q[17] -> rec[0];
measure q[18] -> rec[1];
measure q[19] -> rec[2];
measure q[20] -> rec[3];
measure q[21] -> rec[4];
measure q[22] -> rec[5];
measure q[23] -> rec[6];
measure q[24] -> rec[7];
measure q[25] -> rec[8];
measure q[26] -> rec[9];
measure q[27] -> rec[10];
measure q[28] -> rec[11];
measure q[29] -> rec[12];
measure q[30] -> rec[13];
measure q[31] -> rec[14];
measure q[32] -> rec[15];
