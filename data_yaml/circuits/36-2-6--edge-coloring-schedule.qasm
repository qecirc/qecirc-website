OPENQASM 2.0;
include "qelib1.inc";

qreg q[72];
creg rec[36];

reset q[36]; h q[36]; // decomposed RX
reset q[37]; h q[37]; // decomposed RX
reset q[38]; h q[38]; // decomposed RX
reset q[39]; h q[39]; // decomposed RX
reset q[40]; h q[40]; // decomposed RX
reset q[41]; h q[41]; // decomposed RX
reset q[42]; h q[42]; // decomposed RX
reset q[43]; h q[43]; // decomposed RX
reset q[44]; h q[44]; // decomposed RX
reset q[45]; h q[45]; // decomposed RX
reset q[46]; h q[46]; // decomposed RX
reset q[47]; h q[47]; // decomposed RX
reset q[48]; h q[48]; // decomposed RX
reset q[49]; h q[49]; // decomposed RX
reset q[50]; h q[50]; // decomposed RX
reset q[51]; h q[51]; // decomposed RX
reset q[52]; h q[52]; // decomposed RX
reset q[53]; h q[53]; // decomposed RX
reset q[54]; h q[54]; // decomposed RX
reset q[55]; h q[55]; // decomposed RX
reset q[56]; h q[56]; // decomposed RX
reset q[57]; h q[57]; // decomposed RX
reset q[58]; h q[58]; // decomposed RX
reset q[59]; h q[59]; // decomposed RX
reset q[60]; h q[60]; // decomposed RX
reset q[61]; h q[61]; // decomposed RX
reset q[62]; h q[62]; // decomposed RX
reset q[63]; h q[63]; // decomposed RX
reset q[64]; h q[64]; // decomposed RX
reset q[65]; h q[65]; // decomposed RX
reset q[66]; h q[66]; // decomposed RX
reset q[67]; h q[67]; // decomposed RX
reset q[68]; h q[68]; // decomposed RX
reset q[69]; h q[69]; // decomposed RX
reset q[70]; h q[70]; // decomposed RX
reset q[71]; h q[71]; // decomposed RX
barrier q;

cx q[36], q[32];
cx q[37], q[20];
cx q[38], q[17];
cx q[39], q[11];
cx q[40], q[10];
cx q[41], q[31];
cx q[42], q[9];
cx q[43], q[8];
cx q[44], q[7];
cx q[45], q[4];
cx q[46], q[3];
cx q[47], q[28];
cx q[48], q[2];
cx q[49], q[1];
cx q[50], q[0];
cx q[51], q[23];
cx q[52], q[30];
cx q[53], q[33];
cz q[54], q[21];
cz q[55], q[18];
cz q[56], q[35];
cz q[57], q[12];
cz q[58], q[24];
cz q[59], q[19];
cz q[60], q[13];
cz q[61], q[25];
cz q[62], q[27];
cz q[63], q[5];
cz q[64], q[14];
cz q[65], q[26];
cz q[66], q[6];
cz q[67], q[15];
cz q[68], q[16];
cz q[69], q[34];
cz q[70], q[22];
cz q[71], q[29];
barrier q;

barrier q;

cx q[36], q[35];
cx q[37], q[21];
cx q[38], q[18];
cx q[39], q[12];
cx q[40], q[24];
cx q[41], q[19];
cx q[42], q[27];
cx q[43], q[13];
cx q[44], q[25];
cx q[45], q[5];
cx q[46], q[14];
cx q[47], q[26];
cx q[48], q[16];
cx q[49], q[6];
cx q[50], q[15];
cx q[51], q[34];
cx q[52], q[22];
cx q[53], q[29];
cz q[54], q[32];
cz q[55], q[20];
cz q[56], q[17];
cz q[57], q[31];
cz q[58], q[11];
cz q[59], q[10];
cz q[60], q[9];
cz q[61], q[8];
cz q[62], q[7];
cz q[63], q[28];
cz q[64], q[4];
cz q[65], q[3];
cz q[66], q[2];
cz q[67], q[1];
cz q[68], q[0];
cz q[69], q[33];
cz q[70], q[23];
cz q[71], q[30];
barrier q;

barrier q;

cx q[36], q[34];
cx q[37], q[22];
cx q[38], q[29];
cx q[39], q[21];
cx q[40], q[18];
cx q[41], q[35];
cx q[42], q[12];
cx q[43], q[24];
cx q[44], q[19];
cx q[45], q[13];
cx q[46], q[25];
cx q[47], q[27];
cx q[48], q[5];
cx q[49], q[14];
cx q[50], q[26];
cx q[51], q[6];
cx q[52], q[15];
cx q[53], q[16];
cz q[54], q[23];
cz q[55], q[30];
cz q[56], q[33];
cz q[57], q[32];
cz q[58], q[20];
cz q[59], q[17];
cz q[60], q[11];
cz q[61], q[10];
cz q[62], q[31];
cz q[63], q[9];
cz q[64], q[8];
cz q[65], q[7];
cz q[66], q[4];
cz q[67], q[3];
cz q[68], q[28];
cz q[69], q[2];
cz q[70], q[1];
cz q[71], q[0];
barrier q;

barrier q;

cx q[36], q[33];
cx q[37], q[23];
cx q[38], q[30];
cx q[39], q[32];
cx q[40], q[20];
cx q[41], q[17];
cx q[42], q[31];
cx q[43], q[11];
cx q[44], q[10];
cx q[45], q[9];
cx q[46], q[8];
cx q[47], q[7];
cx q[48], q[28];
cx q[49], q[4];
cx q[50], q[3];
cx q[51], q[2];
cx q[52], q[1];
cx q[53], q[0];
cz q[54], q[34];
cz q[55], q[22];
cz q[56], q[29];
cz q[57], q[35];
cz q[58], q[21];
cz q[59], q[18];
cz q[60], q[12];
cz q[61], q[24];
cz q[62], q[19];
cz q[63], q[27];
cz q[64], q[13];
cz q[65], q[25];
cz q[66], q[5];
cz q[67], q[14];
cz q[68], q[26];
cz q[69], q[16];
cz q[70], q[6];
cz q[71], q[15];
barrier q;

h q[36]; measure q[36] -> rec[0]; h q[36]; // decomposed MX
h q[37]; measure q[37] -> rec[1]; h q[37]; // decomposed MX
h q[38]; measure q[38] -> rec[2]; h q[38]; // decomposed MX
h q[39]; measure q[39] -> rec[3]; h q[39]; // decomposed MX
h q[40]; measure q[40] -> rec[4]; h q[40]; // decomposed MX
h q[41]; measure q[41] -> rec[5]; h q[41]; // decomposed MX
h q[42]; measure q[42] -> rec[6]; h q[42]; // decomposed MX
h q[43]; measure q[43] -> rec[7]; h q[43]; // decomposed MX
h q[44]; measure q[44] -> rec[8]; h q[44]; // decomposed MX
h q[45]; measure q[45] -> rec[9]; h q[45]; // decomposed MX
h q[46]; measure q[46] -> rec[10]; h q[46]; // decomposed MX
h q[47]; measure q[47] -> rec[11]; h q[47]; // decomposed MX
h q[48]; measure q[48] -> rec[12]; h q[48]; // decomposed MX
h q[49]; measure q[49] -> rec[13]; h q[49]; // decomposed MX
h q[50]; measure q[50] -> rec[14]; h q[50]; // decomposed MX
h q[51]; measure q[51] -> rec[15]; h q[51]; // decomposed MX
h q[52]; measure q[52] -> rec[16]; h q[52]; // decomposed MX
h q[53]; measure q[53] -> rec[17]; h q[53]; // decomposed MX
h q[54]; measure q[54] -> rec[18]; h q[54]; // decomposed MX
h q[55]; measure q[55] -> rec[19]; h q[55]; // decomposed MX
h q[56]; measure q[56] -> rec[20]; h q[56]; // decomposed MX
h q[57]; measure q[57] -> rec[21]; h q[57]; // decomposed MX
h q[58]; measure q[58] -> rec[22]; h q[58]; // decomposed MX
h q[59]; measure q[59] -> rec[23]; h q[59]; // decomposed MX
h q[60]; measure q[60] -> rec[24]; h q[60]; // decomposed MX
h q[61]; measure q[61] -> rec[25]; h q[61]; // decomposed MX
h q[62]; measure q[62] -> rec[26]; h q[62]; // decomposed MX
h q[63]; measure q[63] -> rec[27]; h q[63]; // decomposed MX
h q[64]; measure q[64] -> rec[28]; h q[64]; // decomposed MX
h q[65]; measure q[65] -> rec[29]; h q[65]; // decomposed MX
h q[66]; measure q[66] -> rec[30]; h q[66]; // decomposed MX
h q[67]; measure q[67] -> rec[31]; h q[67]; // decomposed MX
h q[68]; measure q[68] -> rec[32]; h q[68]; // decomposed MX
h q[69]; measure q[69] -> rec[33]; h q[69]; // decomposed MX
h q[70]; measure q[70] -> rec[34]; h q[70]; // decomposed MX
h q[71]; measure q[71] -> rec[35]; h q[71]; // decomposed MX
