OPENQASM 2.0;
include "qelib1.inc";

qreg q[150];
creg rec[133];

h q[23];
h q[21];
h q[17];
h q[12];
h q[11];
h q[10];
h q[8];
h q[6];
h q[5];
h q[4];
h q[3];
h q[2];
h q[20];
h q[0];
h q[27];
h q[45];
h q[46];
h q[47];
h q[48];
h q[49];
h q[50];
h q[51];
h q[52];
h q[53];
h q[54];
h q[55];
h q[56];
h q[57];
h q[58];
h q[59];
h q[60];
h q[61];
h q[62];
h q[63];
h q[64];
h q[65];
h q[66];
h q[67];
h q[68];
h q[69];
h q[70];
h q[71];
h q[72];
h q[73];
h q[74];
h q[75];
h q[76];
h q[77];
h q[78];
h q[79];
h q[80];
h q[81];
h q[82];
h q[83];
h q[84];
h q[85];
h q[86];
h q[87];
h q[88];
h q[89];
h q[90];
h q[91];
h q[92];
h q[93];
h q[94];
h q[95];
h q[96];
h q[97];
h q[98];
h q[99];
h q[100];
cx q[5], q[24];
cx q[10], q[18];
cx q[2], q[14];
cx q[11], q[29];
cx q[12], q[22];
cx q[0], q[15];
cx q[18], q[25];
cx q[5], q[1];
cx q[10], q[9];
cx q[22], q[16];
cx q[4], q[29];
cx q[6], q[14];
cx q[12], q[30];
cx q[21], q[11];
cx q[15], q[19];
cx q[9], q[2];
cx q[5], q[26];
cx q[8], q[1];
cx q[17], q[10];
cx q[23], q[25];
cx q[0], q[18];
cx q[3], q[12];
cx q[4], q[13];
cx q[6], q[28];
cx q[14], q[24];
cx q[16], q[9];
cx q[22], q[1];
cx q[30], q[23];
cx q[27], q[5];
cx q[20], q[17];
cx q[26], q[21];
cx q[8], q[7];
cx q[3], q[13];
cx q[10], q[19];
cx q[12], q[4];
cx q[27], q[28];
cx q[20], q[0];
cx q[1], q[9];
cx q[25], q[8];
cx q[29], q[30];
cx q[2], q[26];
cx q[5], q[6];
cx q[11], q[16];
cx q[17], q[15];
cx q[21], q[22];
cx q[23], q[7];
cx q[10], q[32];
cx q[12], q[42];
cx q[21], q[31];
cx q[49], q[32];
cx q[7], q[33];
cx q[23], q[34];
cx q[10], q[35];
cx q[6], q[41];
cx q[77], q[42];
cx q[89], q[17];
cx q[45], q[31];
cx q[20], q[32];
cx q[50], q[33];
cx q[54], q[34];
cx q[58], q[35];
cx q[23], q[36];
cx q[10], q[39];
cx q[76], q[41];
cx q[6], q[43];
cx q[89], q[101];
cx q[5], q[31];
cx q[18], q[32];
cx q[1], q[33];
cx q[21], q[34];
cx q[62], q[36];
cx q[23], q[37];
cx q[71], q[39];
cx q[81], q[43];
cx q[46], q[31];
cx q[49], q[32];
cx q[51], q[33];
cx q[55], q[34];
cx q[66], q[37];
cx q[90], q[21];
cx q[91], q[23];
cx q[4], q[31];
h q[49];
cx q[15], q[32];
cx q[26], q[33];
cx q[11], q[34];
cx q[7], q[37];
cx q[90], q[107];
cx q[91], q[111];
cx q[92], q[23];
cx q[97], q[21];
cx q[47], q[31];
measure q[49] -> rec[0]; reset q[49]; // decomposed MR
measure q[32] -> rec[1]; reset q[32]; // decomposed MR
cx q[52], q[33];
cx q[56], q[34];
cx q[67], q[37];
cx q[7], q[39];
cx q[11], q[42];
cx q[90], q[12];
cx q[91], q[17];
cx q[92], q[115];
cx q[96], q[23];
cx q[97], q[132];
cx q[99], q[21];
cx q[3], q[31];
cx q[28], q[33];
cx q[8], q[34];
cx q[72], q[39];
cx q[78], q[42];
measure q[32] -> rec[2]; reset q[32]; // decomposed MR
cx q[90], q[108];
cx q[91], q[112];
cx q[93], q[12];
cx q[96], q[131];
cx q[98], q[23];
cx q[99], q[140];
cx q[48], q[31];
cx q[53], q[33];
cx q[57], q[34];
cx q[8], q[36];
cx q[90], q[11];
cx q[93], q[119];
cx q[95], q[12];
cx q[98], q[136];
cx q[100], q[23];
cx q[45], q[31];
cx q[50], q[33];
cx q[54], q[34];
cx q[63], q[36];
cx q[8], q[40];
cx q[90], q[109];
cx q[93], q[11];
cx q[95], q[127];
cx q[100], q[146];
h q[45];
cx q[27], q[31];
h q[50];
h q[54];
cx q[4], q[34];
cx q[5], q[36];
cx q[75], q[40];
cx q[89], q[8];
cx q[93], q[120];
cx q[94], q[11];
cx q[100], q[12];
measure q[45] -> rec[3]; reset q[45]; // decomposed MR
cx q[47], q[31];
measure q[50] -> rec[4]; reset q[50]; // decomposed MR
cx q[27], q[33];
measure q[54] -> rec[5]; reset q[54]; // decomposed MR
cx q[56], q[34];
cx q[4], q[35];
cx q[64], q[36];
cx q[5], q[37];
cx q[7], q[40];
cx q[89], q[106];
cx q[94], q[123];
cx q[95], q[11];
cx q[100], q[147];
h q[47];
cx q[16], q[31];
cx q[52], q[33];
h q[56];
cx q[3], q[34];
cx q[59], q[35];
cx q[2], q[36];
cx q[68], q[37];
cx q[5], q[43];
cx q[7], q[44];
cx q[89], q[102];
cx q[95], q[128];
cx q[97], q[11];
measure q[47] -> rec[6]; reset q[47]; // decomposed MR
cx q[29], q[31];
h q[52];
cx q[14], q[33];
measure q[56] -> rec[7]; reset q[56]; // decomposed MR
cx q[9], q[34];
cx q[13], q[35];
cx q[65], q[36];
cx q[4], q[37];
cx q[82], q[43];
cx q[85], q[44];
cx q[89], q[5];
cx q[90], q[7];
cx q[97], q[133];
cx q[99], q[11];
cx q[46], q[31];
measure q[52] -> rec[8]; reset q[52]; // decomposed MR
cx q[25], q[33];
cx q[55], q[34];
cx q[60], q[35];
cx q[62], q[36];
cx q[69], q[37];
cx q[4], q[38];
cx q[90], q[110];
cx q[91], q[7];
cx q[92], q[5];
cx q[97], q[8];
cx q[99], q[145];
h q[46];
cx q[48], q[31];
cx q[51], q[33];
h q[55];
cx q[57], q[34];
cx q[1], q[35];
h q[62];
cx q[66], q[37];
cx q[70], q[38];
cx q[4], q[43];
cx q[90], q[107];
cx q[91], q[113];
cx q[92], q[116];
cx q[93], q[7];
cx q[97], q[134];
cx q[98], q[8];
cx q[99], q[141];
measure q[46] -> rec[9]; reset q[46]; // decomposed MR
h q[48];
measure q[31] -> rec[10]; reset q[31]; // decomposed MR
h q[51];
cx q[53], q[33];
measure q[55] -> rec[11]; reset q[55]; // decomposed MR
h q[57];
cx q[29], q[34];
cx q[61], q[35];
measure q[62] -> rec[12]; reset q[62]; // decomposed MR
cx q[1], q[36];
h q[66];
cx q[13], q[37];
cx q[83], q[43];
cx q[4], q[44];
measure q[107] -> rec[13]; reset q[107]; // decomposed MR
cx q[91], q[6];
cx q[93], q[121];
cx q[97], q[7];
cx q[98], q[137];
measure q[48] -> rec[14]; reset q[48]; // decomposed MR
measure q[51] -> rec[15]; reset q[51]; // decomposed MR
h q[53];
measure q[33] -> rec[16]; reset q[33]; // decomposed MR
measure q[57] -> rec[17]; reset q[57]; // decomposed MR
measure q[34] -> rec[18]; reset q[34]; // decomposed MR
cx q[58], q[35];
cx q[64], q[36];
measure q[66] -> rec[19]; reset q[66]; // decomposed MR
cx q[68], q[37];
cx q[13], q[38];
cx q[86], q[44];
measure q[31] -> rec[20]; reset q[31]; // decomposed MR
cx q[89], q[4];
cx q[91], q[114];
cx q[94], q[6];
cx q[97], q[135];
cx q[98], q[7];
measure q[53] -> rec[21]; reset q[53]; // decomposed MR
h q[58];
cx q[9], q[35];
h q[64];
cx q[28], q[36];
h q[68];
cx q[1], q[37];
cx q[30], q[38];
cx q[13], q[42];
measure q[33] -> rec[22]; reset q[33]; // decomposed MR
measure q[34] -> rec[23]; reset q[34]; // decomposed MR
cx q[89], q[103];
cx q[91], q[111];
cx q[92], q[4];
cx q[94], q[124];
cx q[97], q[132];
cx q[98], q[138];
cx q[99], q[6];
cx q[100], q[7];
measure q[58] -> rec[24]; reset q[58]; // decomposed MR
cx q[60], q[35];
measure q[64] -> rec[25]; reset q[64]; // decomposed MR
cx q[14], q[36];
measure q[68] -> rec[26]; reset q[68]; // decomposed MR
cx q[27], q[37];
cx q[70], q[38];
cx q[1], q[39];
cx q[28], q[41];
cx q[79], q[42];
cx q[13], q[43];
measure q[111] -> rec[27]; reset q[111]; // decomposed MR
cx q[92], q[117];
cx q[94], q[4];
measure q[132] -> rec[28]; reset q[132]; // decomposed MR
cx q[99], q[5];
cx q[100], q[148];
h q[60];
cx q[0], q[35];
cx q[63], q[36];
cx q[67], q[37];
h q[70];
cx q[29], q[38];
cx q[73], q[39];
cx q[1], q[40];
cx q[84], q[43];
cx q[13], q[44];
cx q[92], q[2];
cx q[94], q[125];
cx q[95], q[4];
cx q[99], q[142];
measure q[60] -> rec[29]; reset q[60]; // decomposed MR
cx q[15], q[35];
h q[63];
cx q[65], q[36];
h q[67];
cx q[69], q[37];
measure q[70] -> rec[30]; reset q[70]; // decomposed MR
measure q[38] -> rec[31]; reset q[38]; // decomposed MR
cx q[0], q[39];
cx q[75], q[40];
cx q[81], q[43];
cx q[87], q[44];
cx q[89], q[13];
cx q[92], q[118];
cx q[94], q[2];
cx q[95], q[129];
cx q[98], q[4];
cx q[59], q[35];
measure q[63] -> rec[32]; reset q[63]; // decomposed MR
h q[65];
measure q[36] -> rec[33]; reset q[36]; // decomposed MR
measure q[67] -> rec[34]; reset q[67]; // decomposed MR
h q[69];
measure q[37] -> rec[35]; reset q[37]; // decomposed MR
cx q[74], q[39];
h q[75];
cx q[9], q[40];
h q[81];
cx q[1], q[43];
measure q[38] -> rec[36]; reset q[38]; // decomposed MR
cx q[89], q[106];
cx q[90], q[13];
cx q[92], q[115];
cx q[94], q[126];
cx q[95], q[3];
cx q[98], q[139];
h q[59];
cx q[61], q[35];
measure q[65] -> rec[37]; reset q[65]; // decomposed MR
measure q[69] -> rec[38]; reset q[69]; // decomposed MR
cx q[71], q[39];
measure q[75] -> rec[39]; reset q[75]; // decomposed MR
measure q[40] -> rec[40]; reset q[40]; // decomposed MR
measure q[81] -> rec[41]; reset q[81]; // decomposed MR
cx q[83], q[43];
measure q[36] -> rec[42]; reset q[36]; // decomposed MR
measure q[37] -> rec[43]; reset q[37]; // decomposed MR
measure q[106] -> rec[44]; reset q[106]; // decomposed MR
cx q[89], q[1];
cx q[90], q[109];
measure q[115] -> rec[45]; reset q[115]; // decomposed MR
cx q[92], q[13];
cx q[94], q[123];
cx q[95], q[130];
cx q[98], q[136];
measure q[59] -> rec[46]; reset q[59]; // decomposed MR
h q[61];
measure q[35] -> rec[47]; reset q[35]; // decomposed MR
h q[71];
cx q[14], q[39];
h q[83];
cx q[26], q[43];
measure q[40] -> rec[48]; reset q[40]; // decomposed MR
cx q[89], q[104];
measure q[109] -> rec[49]; reset q[109]; // decomposed MR
cx q[92], q[117];
cx q[93], q[13];
measure q[123] -> rec[50]; reset q[123]; // decomposed MR
cx q[95], q[127];
cx q[96], q[1];
measure q[136] -> rec[51]; reset q[136]; // decomposed MR
measure q[61] -> rec[52]; reset q[61]; // decomposed MR
measure q[71] -> rec[53]; reset q[71]; // decomposed MR
cx q[73], q[39];
cx q[14], q[41];
measure q[83] -> rec[54]; reset q[83]; // decomposed MR
cx q[9], q[43];
measure q[35] -> rec[55]; reset q[35]; // decomposed MR
cx q[89], q[26];
measure q[117] -> rec[56]; reset q[117]; // decomposed MR
cx q[93], q[122];
cx q[94], q[13];
measure q[127] -> rec[57]; reset q[127]; // decomposed MR
cx q[97], q[1];
h q[73];
cx q[15], q[39];
cx q[76], q[41];
cx q[14], q[42];
cx q[82], q[43];
cx q[9], q[44];
cx q[89], q[103];
cx q[93], q[119];
cx q[94], q[125];
cx q[95], q[13];
cx q[97], q[134];
cx q[99], q[1];
measure q[73] -> rec[58]; reset q[73]; // decomposed MR
cx q[25], q[39];
h q[76];
cx q[80], q[42];
h q[82];
cx q[84], q[43];
cx q[88], q[44];
measure q[103] -> rec[59]; reset q[103]; // decomposed MR
cx q[89], q[28];
cx q[90], q[9];
measure q[119] -> rec[60]; reset q[119]; // decomposed MR
measure q[125] -> rec[61]; reset q[125]; // decomposed MR
cx q[94], q[26];
cx q[95], q[129];
measure q[134] -> rec[62]; reset q[134]; // decomposed MR
cx q[98], q[13];
cx q[99], q[145];
cx q[72], q[39];
measure q[76] -> rec[63]; reset q[76]; // decomposed MR
cx q[77], q[42];
measure q[82] -> rec[64]; reset q[82]; // decomposed MR
h q[84];
cx q[85], q[44];
cx q[89], q[105];
cx q[91], q[9];
measure q[129] -> rec[65]; reset q[129]; // decomposed MR
cx q[98], q[138];
measure q[145] -> rec[66]; reset q[145]; // decomposed MR
cx q[99], q[26];
cx q[100], q[13];
h q[72];
cx q[74], q[39];
h q[77];
cx q[22], q[42];
measure q[84] -> rec[67]; reset q[84]; // decomposed MR
h q[85];
cx q[14], q[44];
cx q[89], q[0];
cx q[91], q[113];
cx q[93], q[9];
measure q[138] -> rec[68]; reset q[138]; // decomposed MR
cx q[99], q[143];
cx q[100], q[149];
measure q[72] -> rec[69]; reset q[72]; // decomposed MR
h q[74];
cx q[24], q[39];
measure q[77] -> rec[70]; reset q[77]; // decomposed MR
cx q[79], q[42];
measure q[85] -> rec[71]; reset q[85]; // decomposed MR
cx q[87], q[44];
cx q[89], q[104];
measure q[113] -> rec[72]; reset q[113]; // decomposed MR
cx q[91], q[28];
cx q[93], q[121];
cx q[96], q[9];
cx q[100], q[146];
measure q[74] -> rec[73]; reset q[74]; // decomposed MR
measure q[39] -> rec[74]; reset q[39]; // decomposed MR
cx q[24], q[41];
h q[79];
cx q[29], q[42];
h q[87];
cx q[25], q[44];
measure q[104] -> rec[75]; reset q[104]; // decomposed MR
cx q[89], q[19];
cx q[91], q[0];
cx q[92], q[28];
measure q[121] -> rec[76]; reset q[121]; // decomposed MR
cx q[93], q[30];
cx q[96], q[131];
cx q[97], q[9];
measure q[146] -> rec[77]; reset q[146]; // decomposed MR
cx q[100], q[1];
measure q[41] -> rec[78]; reset q[41]; // decomposed MR
measure q[79] -> rec[79]; reset q[79]; // decomposed MR
cx q[24], q[42];
measure q[87] -> rec[80]; reset q[87]; // decomposed MR
measure q[39] -> rec[81]; reset q[39]; // decomposed MR
cx q[89], q[101];
cx q[90], q[29];
cx q[91], q[112];
cx q[93], q[22];
cx q[94], q[28];
cx q[95], q[30];
measure q[131] -> rec[82]; reset q[131]; // decomposed MR
cx q[99], q[9];
cx q[100], q[148];
cx q[78], q[42];
cx q[24], q[43];
measure q[41] -> rec[83]; reset q[41]; // decomposed MR
measure q[101] -> rec[84]; reset q[101]; // decomposed MR
cx q[89], q[25];
cx q[90], q[108];
measure q[112] -> rec[85]; reset q[112]; // decomposed MR
cx q[91], q[114];
cx q[93], q[120];
cx q[94], q[124];
cx q[97], q[22];
cx q[98], q[30];
cx q[99], q[142];
measure q[148] -> rec[86]; reset q[148]; // decomposed MR
h q[78];
cx q[80], q[42];
measure q[43] -> rec[87]; reset q[43]; // decomposed MR
cx q[24], q[44];
cx q[89], q[105];
measure q[108] -> rec[88]; reset q[108]; // decomposed MR
cx q[90], q[110];
measure q[114] -> rec[89]; reset q[114]; // decomposed MR
cx q[91], q[19];
measure q[120] -> rec[90]; reset q[120]; // decomposed MR
cx q[93], q[122];
measure q[124] -> rec[91]; reset q[124]; // decomposed MR
cx q[94], q[126];
cx q[97], q[133];
measure q[142] -> rec[92]; reset q[142]; // decomposed MR
cx q[99], q[30];
measure q[78] -> rec[93]; reset q[78]; // decomposed MR
h q[80];
measure q[42] -> rec[94]; reset q[42]; // decomposed MR
cx q[86], q[44];
measure q[43] -> rec[95]; reset q[43]; // decomposed MR
measure q[105] -> rec[96]; reset q[105]; // decomposed MR
cx q[89], q[102];
measure q[110] -> rec[97]; reset q[110]; // decomposed MR
cx q[90], q[25];
h q[91];
measure q[122] -> rec[98]; reset q[122]; // decomposed MR
measure q[126] -> rec[99]; reset q[126]; // decomposed MR
cx q[94], q[16];
measure q[133] -> rec[100]; reset q[133]; // decomposed MR
cx q[97], q[135];
cx q[99], q[144];
measure q[80] -> rec[101]; reset q[80]; // decomposed MR
h q[86];
cx q[88], q[44];
measure q[42] -> rec[102]; reset q[42]; // decomposed MR
measure q[102] -> rec[103]; reset q[102]; // decomposed MR
cx q[89], q[24];
h q[90];
measure q[91] -> rec[104]; reset q[91]; // decomposed MR
cx q[92], q[25];
h q[94];
cx q[95], q[16];
measure q[135] -> rec[105]; reset q[135]; // decomposed MR
cx q[99], q[22];
measure q[86] -> rec[106]; reset q[86]; // decomposed MR
h q[88];
measure q[44] -> rec[107]; reset q[44]; // decomposed MR
h q[89];
measure q[90] -> rec[108]; reset q[90]; // decomposed MR
cx q[92], q[116];
cx q[93], q[25];
measure q[94] -> rec[109]; reset q[94]; // decomposed MR
cx q[95], q[128];
cx q[97], q[16];
cx q[99], q[143];
cx q[100], q[22];
measure q[88] -> rec[110]; reset q[88]; // decomposed MR
measure q[44] -> rec[111]; reset q[44]; // decomposed MR
measure q[89] -> rec[112]; reset q[89]; // decomposed MR
measure q[116] -> rec[113]; reset q[116]; // decomposed MR
cx q[92], q[118];
h q[93];
measure q[128] -> rec[114]; reset q[128]; // decomposed MR
cx q[95], q[130];
cx q[96], q[25];
h q[97];
measure q[143] -> rec[115]; reset q[143]; // decomposed MR
cx q[99], q[16];
measure q[118] -> rec[116]; reset q[118]; // decomposed MR
cx q[92], q[24];
measure q[93] -> rec[117]; reset q[93]; // decomposed MR
measure q[130] -> rec[118]; reset q[130]; // decomposed MR
cx q[95], q[29];
h q[96];
measure q[97] -> rec[119]; reset q[97]; // decomposed MR
cx q[99], q[140];
cx q[100], q[16];
h q[92];
h q[95];
measure q[96] -> rec[120]; reset q[96]; // decomposed MR
cx q[98], q[29];
measure q[140] -> rec[121]; reset q[140]; // decomposed MR
cx q[100], q[147];
measure q[92] -> rec[122]; reset q[92]; // decomposed MR
measure q[95] -> rec[123]; reset q[95]; // decomposed MR
cx q[98], q[137];
cx q[99], q[29];
measure q[147] -> rec[124]; reset q[147]; // decomposed MR
cx q[100], q[149];
measure q[137] -> rec[125]; reset q[137]; // decomposed MR
cx q[98], q[139];
cx q[99], q[144];
measure q[149] -> rec[126]; reset q[149]; // decomposed MR
cx q[100], q[29];
measure q[139] -> rec[127]; reset q[139]; // decomposed MR
cx q[98], q[25];
measure q[144] -> rec[128]; reset q[144]; // decomposed MR
cx q[99], q[141];
h q[100];
h q[98];
measure q[141] -> rec[129]; reset q[141]; // decomposed MR
cx q[99], q[24];
measure q[100] -> rec[130]; reset q[100]; // decomposed MR
measure q[98] -> rec[131]; reset q[98]; // decomposed MR
h q[99];
measure q[99] -> rec[132]; reset q[99]; // decomposed MR
