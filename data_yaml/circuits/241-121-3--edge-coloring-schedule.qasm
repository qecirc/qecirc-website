OPENQASM 2.0;
include "qelib1.inc";

qreg q[361];
creg rec[120];

reset q[241]; h q[241]; // decomposed RX
reset q[242]; h q[242]; // decomposed RX
reset q[243]; h q[243]; // decomposed RX
reset q[244]; h q[244]; // decomposed RX
reset q[245]; h q[245]; // decomposed RX
reset q[246]; h q[246]; // decomposed RX
reset q[247]; h q[247]; // decomposed RX
reset q[248]; h q[248]; // decomposed RX
reset q[249]; h q[249]; // decomposed RX
reset q[250]; h q[250]; // decomposed RX
reset q[251]; h q[251]; // decomposed RX
reset q[252]; h q[252]; // decomposed RX
reset q[253]; h q[253]; // decomposed RX
reset q[254]; h q[254]; // decomposed RX
reset q[255]; h q[255]; // decomposed RX
reset q[256]; h q[256]; // decomposed RX
reset q[257]; h q[257]; // decomposed RX
reset q[258]; h q[258]; // decomposed RX
reset q[259]; h q[259]; // decomposed RX
reset q[260]; h q[260]; // decomposed RX
reset q[261]; h q[261]; // decomposed RX
reset q[262]; h q[262]; // decomposed RX
reset q[263]; h q[263]; // decomposed RX
reset q[264]; h q[264]; // decomposed RX
reset q[265]; h q[265]; // decomposed RX
reset q[266]; h q[266]; // decomposed RX
reset q[267]; h q[267]; // decomposed RX
reset q[268]; h q[268]; // decomposed RX
reset q[269]; h q[269]; // decomposed RX
reset q[270]; h q[270]; // decomposed RX
reset q[271]; h q[271]; // decomposed RX
reset q[272]; h q[272]; // decomposed RX
reset q[273]; h q[273]; // decomposed RX
reset q[274]; h q[274]; // decomposed RX
reset q[275]; h q[275]; // decomposed RX
reset q[276]; h q[276]; // decomposed RX
reset q[277]; h q[277]; // decomposed RX
reset q[278]; h q[278]; // decomposed RX
reset q[279]; h q[279]; // decomposed RX
reset q[280]; h q[280]; // decomposed RX
reset q[281]; h q[281]; // decomposed RX
reset q[282]; h q[282]; // decomposed RX
reset q[283]; h q[283]; // decomposed RX
reset q[284]; h q[284]; // decomposed RX
reset q[285]; h q[285]; // decomposed RX
reset q[286]; h q[286]; // decomposed RX
reset q[287]; h q[287]; // decomposed RX
reset q[288]; h q[288]; // decomposed RX
reset q[289]; h q[289]; // decomposed RX
reset q[290]; h q[290]; // decomposed RX
reset q[291]; h q[291]; // decomposed RX
reset q[292]; h q[292]; // decomposed RX
reset q[293]; h q[293]; // decomposed RX
reset q[294]; h q[294]; // decomposed RX
reset q[295]; h q[295]; // decomposed RX
reset q[296]; h q[296]; // decomposed RX
reset q[297]; h q[297]; // decomposed RX
reset q[298]; h q[298]; // decomposed RX
reset q[299]; h q[299]; // decomposed RX
reset q[300]; h q[300]; // decomposed RX
reset q[301]; h q[301]; // decomposed RX
reset q[302]; h q[302]; // decomposed RX
reset q[303]; h q[303]; // decomposed RX
reset q[304]; h q[304]; // decomposed RX
reset q[305]; h q[305]; // decomposed RX
reset q[306]; h q[306]; // decomposed RX
reset q[307]; h q[307]; // decomposed RX
reset q[308]; h q[308]; // decomposed RX
reset q[309]; h q[309]; // decomposed RX
reset q[310]; h q[310]; // decomposed RX
reset q[311]; h q[311]; // decomposed RX
reset q[312]; h q[312]; // decomposed RX
reset q[313]; h q[313]; // decomposed RX
reset q[314]; h q[314]; // decomposed RX
reset q[315]; h q[315]; // decomposed RX
reset q[316]; h q[316]; // decomposed RX
reset q[317]; h q[317]; // decomposed RX
reset q[318]; h q[318]; // decomposed RX
reset q[319]; h q[319]; // decomposed RX
reset q[320]; h q[320]; // decomposed RX
reset q[321]; h q[321]; // decomposed RX
reset q[322]; h q[322]; // decomposed RX
reset q[323]; h q[323]; // decomposed RX
reset q[324]; h q[324]; // decomposed RX
reset q[325]; h q[325]; // decomposed RX
reset q[326]; h q[326]; // decomposed RX
reset q[327]; h q[327]; // decomposed RX
reset q[328]; h q[328]; // decomposed RX
reset q[329]; h q[329]; // decomposed RX
reset q[330]; h q[330]; // decomposed RX
reset q[331]; h q[331]; // decomposed RX
reset q[332]; h q[332]; // decomposed RX
reset q[333]; h q[333]; // decomposed RX
reset q[334]; h q[334]; // decomposed RX
reset q[335]; h q[335]; // decomposed RX
reset q[336]; h q[336]; // decomposed RX
reset q[337]; h q[337]; // decomposed RX
reset q[338]; h q[338]; // decomposed RX
reset q[339]; h q[339]; // decomposed RX
reset q[340]; h q[340]; // decomposed RX
reset q[341]; h q[341]; // decomposed RX
reset q[342]; h q[342]; // decomposed RX
reset q[343]; h q[343]; // decomposed RX
reset q[344]; h q[344]; // decomposed RX
reset q[345]; h q[345]; // decomposed RX
reset q[346]; h q[346]; // decomposed RX
reset q[347]; h q[347]; // decomposed RX
reset q[348]; h q[348]; // decomposed RX
reset q[349]; h q[349]; // decomposed RX
reset q[350]; h q[350]; // decomposed RX
reset q[351]; h q[351]; // decomposed RX
reset q[352]; h q[352]; // decomposed RX
reset q[353]; h q[353]; // decomposed RX
reset q[354]; h q[354]; // decomposed RX
reset q[355]; h q[355]; // decomposed RX
reset q[356]; h q[356]; // decomposed RX
reset q[357]; h q[357]; // decomposed RX
reset q[358]; h q[358]; // decomposed RX
reset q[359]; h q[359]; // decomposed RX
reset q[360]; h q[360]; // decomposed RX
barrier q;

cx q[241], q[17];
cx q[242], q[15];
cx q[243], q[14];
cx q[244], q[12];
cx q[245], q[11];
cx q[246], q[10];
cx q[247], q[9];
cx q[248], q[7];
cx q[249], q[6];
cx q[250], q[5];
cx q[251], q[4];
cx q[252], q[3];
cx q[253], q[2];
cx q[254], q[1];
cx q[255], q[0];
cx q[256], q[239];
cx q[257], q[230];
cx q[258], q[222];
cx q[259], q[213];
cx q[260], q[205];
cx q[261], q[197];
cx q[262], q[189];
cx q[263], q[180];
cx q[264], q[172];
cx q[265], q[164];
cx q[266], q[156];
cx q[267], q[148];
cx q[268], q[140];
cx q[269], q[132];
cx q[270], q[124];
cx q[271], q[237];
cx q[272], q[228];
cx q[273], q[220];
cx q[274], q[211];
cx q[275], q[203];
cx q[276], q[195];
cx q[277], q[187];
cx q[278], q[178];
cx q[279], q[170];
cx q[280], q[162];
cx q[281], q[154];
cx q[282], q[146];
cx q[283], q[138];
cx q[284], q[130];
cx q[285], q[122];
cx q[286], q[235];
cx q[287], q[226];
cx q[288], q[218];
cx q[289], q[209];
cx q[290], q[201];
cx q[291], q[193];
cx q[292], q[185];
cx q[293], q[176];
cx q[294], q[168];
cx q[295], q[160];
cx q[296], q[152];
cx q[297], q[144];
cx q[298], q[136];
cx q[299], q[128];
cx q[300], q[120];
barrier q;

barrier q;

cz q[325], q[35];
cz q[326], q[44];
cz q[327], q[49];
cz q[328], q[52];
cz q[349], q[8];
cz q[350], q[13];
cz q[351], q[16];
cz q[352], q[18];
cz q[353], q[85];
cz q[354], q[102];
cz q[355], q[111];
cz q[356], q[116];
cz q[357], q[181];
cz q[358], q[214];
cz q[359], q[231];
cz q[360], q[240];
barrier q;

barrier q;

cx q[241], q[113];
cx q[242], q[108];
cx q[243], q[104];
cx q[244], q[99];
cx q[245], q[95];
cx q[246], q[91];
cx q[247], q[87];
cx q[248], q[82];
cx q[249], q[78];
cx q[250], q[74];
cx q[251], q[70];
cx q[252], q[66];
cx q[253], q[62];
cx q[254], q[58];
cx q[255], q[54];
cx q[256], q[235];
cx q[257], q[226];
cx q[258], q[218];
cx q[259], q[209];
cx q[260], q[201];
cx q[261], q[193];
cx q[262], q[185];
cx q[263], q[176];
cx q[264], q[168];
cx q[265], q[160];
cx q[266], q[152];
cx q[267], q[144];
cx q[268], q[136];
cx q[269], q[128];
cx q[270], q[120];
cx q[271], q[239];
cx q[272], q[230];
cx q[273], q[222];
cx q[274], q[213];
cx q[275], q[205];
cx q[276], q[197];
cx q[277], q[189];
cx q[278], q[180];
cx q[279], q[172];
cx q[280], q[164];
cx q[281], q[156];
cx q[282], q[148];
cx q[283], q[140];
cx q[284], q[132];
cx q[285], q[124];
cx q[286], q[237];
cx q[287], q[228];
cx q[288], q[220];
cx q[289], q[211];
cx q[290], q[203];
cx q[291], q[195];
cx q[292], q[187];
cx q[293], q[178];
cx q[294], q[170];
cx q[295], q[162];
cx q[296], q[154];
cx q[297], q[146];
cx q[298], q[138];
cx q[299], q[130];
cx q[300], q[122];
barrier q;

barrier q;

cz q[309], q[85];
cz q[310], q[102];
cz q[311], q[111];
cz q[312], q[116];
cz q[333], q[181];
cz q[334], q[214];
cz q[335], q[231];
cz q[336], q[240];
cz q[353], q[35];
cz q[354], q[44];
cz q[355], q[49];
cz q[356], q[52];
cz q[357], q[8];
cz q[358], q[13];
cz q[359], q[16];
cz q[360], q[18];
barrier q;

barrier q;

cx q[241], q[51];
cx q[242], q[48];
cx q[243], q[46];
cx q[244], q[43];
cx q[245], q[41];
cx q[246], q[39];
cx q[247], q[37];
cx q[248], q[34];
cx q[249], q[32];
cx q[250], q[30];
cx q[251], q[28];
cx q[252], q[26];
cx q[253], q[24];
cx q[254], q[22];
cx q[255], q[20];
cx q[256], q[234];
cx q[257], q[225];
cx q[258], q[217];
cx q[259], q[208];
cx q[260], q[200];
cx q[261], q[192];
cx q[262], q[184];
cx q[263], q[175];
cx q[264], q[167];
cx q[265], q[159];
cx q[266], q[151];
cx q[267], q[143];
cx q[268], q[135];
cx q[269], q[127];
cx q[270], q[119];
cx q[271], q[113];
cx q[272], q[108];
cx q[273], q[104];
cx q[274], q[99];
cx q[275], q[95];
cx q[276], q[91];
cx q[277], q[87];
cx q[278], q[82];
cx q[279], q[78];
cx q[280], q[74];
cx q[281], q[70];
cx q[282], q[66];
cx q[283], q[62];
cx q[284], q[58];
cx q[285], q[54];
cx q[286], q[232];
cx q[287], q[223];
cx q[288], q[215];
cx q[289], q[206];
cx q[290], q[198];
cx q[291], q[190];
cx q[292], q[182];
cx q[293], q[173];
cx q[294], q[165];
cx q[295], q[157];
cx q[296], q[149];
cx q[297], q[141];
cx q[298], q[133];
cx q[299], q[125];
cx q[300], q[117];
barrier q;

barrier q;

cz q[317], q[181];
cz q[318], q[214];
cz q[319], q[231];
cz q[320], q[240];
cz q[321], q[35];
cz q[322], q[44];
cz q[323], q[49];
cz q[324], q[52];
cz q[325], q[85];
cz q[326], q[102];
cz q[327], q[111];
cz q[328], q[116];
cz q[341], q[8];
cz q[342], q[13];
cz q[343], q[16];
cz q[344], q[18];
barrier q;

barrier q;

cx q[241], q[233];
cx q[242], q[224];
cx q[243], q[216];
cx q[244], q[207];
cx q[245], q[199];
cx q[246], q[191];
cx q[247], q[183];
cx q[248], q[174];
cx q[249], q[166];
cx q[250], q[158];
cx q[251], q[150];
cx q[252], q[142];
cx q[253], q[134];
cx q[254], q[126];
cx q[255], q[118];
cx q[256], q[51];
cx q[257], q[48];
cx q[258], q[46];
cx q[259], q[43];
cx q[260], q[41];
cx q[261], q[39];
cx q[262], q[37];
cx q[263], q[34];
cx q[264], q[32];
cx q[265], q[30];
cx q[266], q[28];
cx q[267], q[26];
cx q[268], q[24];
cx q[269], q[22];
cx q[270], q[20];
cx q[271], q[114];
cx q[272], q[109];
cx q[273], q[105];
cx q[274], q[100];
cx q[275], q[96];
cx q[276], q[92];
cx q[277], q[88];
cx q[278], q[83];
cx q[279], q[79];
cx q[280], q[75];
cx q[281], q[71];
cx q[282], q[67];
cx q[283], q[63];
cx q[284], q[59];
cx q[285], q[55];
cx q[286], q[238];
cx q[287], q[229];
cx q[288], q[221];
cx q[289], q[212];
cx q[290], q[204];
cx q[291], q[196];
cx q[292], q[188];
cx q[293], q[179];
cx q[294], q[171];
cx q[295], q[163];
cx q[296], q[155];
cx q[297], q[147];
cx q[298], q[139];
cx q[299], q[131];
cx q[300], q[123];
barrier q;

barrier q;

cz q[305], q[85];
cz q[306], q[102];
cz q[307], q[111];
cz q[308], q[116];
cz q[309], q[181];
cz q[310], q[214];
cz q[311], q[231];
cz q[312], q[240];
cz q[313], q[35];
cz q[314], q[44];
cz q[315], q[49];
cz q[316], q[52];
cz q[353], q[8];
cz q[354], q[13];
cz q[355], q[16];
cz q[356], q[18];
barrier q;

barrier q;

cx q[248], q[8];
cx q[251], q[16];
cx q[253], q[18];
cx q[255], q[13];
cx q[263], q[35];
cx q[266], q[49];
cx q[268], q[52];
cx q[270], q[44];
cx q[278], q[85];
cx q[281], q[111];
cx q[283], q[116];
cx q[285], q[102];
cx q[293], q[181];
cx q[296], q[231];
cx q[298], q[240];
cx q[300], q[214];
cz q[301], q[173];
cz q[302], q[117];
cz q[303], q[149];
cz q[304], q[133];
cz q[305], q[81];
cz q[306], q[53];
cz q[307], q[69];
cz q[308], q[61];
cz q[309], q[177];
cz q[310], q[121];
cz q[311], q[153];
cz q[312], q[137];
cz q[313], q[33];
cz q[314], q[19];
cz q[315], q[27];
cz q[316], q[23];
cz q[317], q[175];
cz q[318], q[119];
cz q[319], q[151];
cz q[320], q[135];
cz q[321], q[83];
cz q[322], q[55];
cz q[323], q[71];
cz q[324], q[63];
cz q[325], q[179];
cz q[326], q[123];
cz q[327], q[155];
cz q[328], q[139];
cz q[329], q[7];
cz q[330], q[0];
cz q[331], q[4];
cz q[332], q[2];
cz q[333], q[174];
cz q[334], q[118];
cz q[335], q[150];
cz q[336], q[134];
cz q[337], q[82];
cz q[338], q[54];
cz q[339], q[70];
cz q[340], q[62];
cz q[341], q[178];
cz q[342], q[122];
cz q[343], q[154];
cz q[344], q[138];
cz q[345], q[34];
cz q[346], q[20];
cz q[347], q[28];
cz q[348], q[24];
cz q[349], q[176];
cz q[350], q[120];
cz q[351], q[152];
cz q[352], q[136];
cz q[353], q[84];
cz q[354], q[56];
cz q[355], q[72];
cz q[356], q[64];
cz q[357], q[180];
cz q[358], q[124];
cz q[359], q[156];
cz q[360], q[140];
barrier q;

barrier q;

cx q[250], q[8];
cx q[251], q[18];
cx q[253], q[13];
cx q[255], q[16];
cx q[265], q[35];
cx q[266], q[52];
cx q[268], q[44];
cx q[270], q[49];
cx q[280], q[85];
cx q[281], q[116];
cx q[283], q[102];
cx q[285], q[111];
cx q[295], q[181];
cx q[296], q[240];
cx q[298], q[214];
cx q[300], q[231];
cz q[301], q[157];
cz q[302], q[133];
cz q[303], q[117];
cz q[304], q[149];
cz q[305], q[73];
cz q[306], q[61];
cz q[307], q[53];
cz q[308], q[69];
cz q[309], q[161];
cz q[310], q[137];
cz q[311], q[121];
cz q[312], q[153];
cz q[313], q[29];
cz q[314], q[23];
cz q[315], q[19];
cz q[316], q[27];
cz q[317], q[159];
cz q[318], q[135];
cz q[319], q[119];
cz q[320], q[151];
cz q[321], q[75];
cz q[322], q[63];
cz q[323], q[55];
cz q[324], q[71];
cz q[325], q[163];
cz q[326], q[139];
cz q[327], q[123];
cz q[328], q[155];
cz q[329], q[5];
cz q[330], q[2];
cz q[331], q[0];
cz q[332], q[4];
cz q[333], q[158];
cz q[334], q[134];
cz q[335], q[118];
cz q[336], q[150];
cz q[337], q[74];
cz q[338], q[62];
cz q[339], q[54];
cz q[340], q[70];
cz q[341], q[162];
cz q[342], q[138];
cz q[343], q[122];
cz q[344], q[154];
cz q[345], q[30];
cz q[346], q[24];
cz q[347], q[20];
cz q[348], q[28];
cz q[349], q[160];
cz q[350], q[136];
cz q[351], q[120];
cz q[352], q[152];
cz q[353], q[76];
cz q[354], q[64];
cz q[355], q[56];
cz q[356], q[72];
cz q[357], q[164];
cz q[358], q[140];
cz q[359], q[124];
cz q[360], q[156];
barrier q;

barrier q;

cx q[241], q[18];
cx q[245], q[13];
cx q[250], q[16];
cx q[252], q[8];
cx q[256], q[52];
cx q[260], q[44];
cx q[265], q[49];
cx q[267], q[35];
cx q[271], q[116];
cx q[275], q[102];
cx q[280], q[111];
cx q[282], q[85];
cx q[286], q[240];
cx q[290], q[214];
cx q[295], q[231];
cx q[297], q[181];
cz q[301], q[141];
cz q[302], q[198];
cz q[303], q[157];
cz q[304], q[232];
cz q[305], q[65];
cz q[306], q[94];
cz q[307], q[73];
cz q[308], q[112];
cz q[309], q[145];
cz q[310], q[202];
cz q[311], q[161];
cz q[312], q[236];
cz q[313], q[25];
cz q[314], q[40];
cz q[315], q[29];
cz q[316], q[50];
cz q[317], q[143];
cz q[318], q[200];
cz q[319], q[159];
cz q[320], q[234];
cz q[321], q[67];
cz q[322], q[96];
cz q[323], q[75];
cz q[324], q[114];
cz q[325], q[147];
cz q[326], q[204];
cz q[327], q[163];
cz q[328], q[238];
cz q[329], q[3];
cz q[330], q[11];
cz q[331], q[5];
cz q[332], q[17];
cz q[333], q[142];
cz q[334], q[199];
cz q[335], q[158];
cz q[336], q[233];
cz q[337], q[66];
cz q[338], q[95];
cz q[339], q[74];
cz q[340], q[113];
cz q[341], q[146];
cz q[342], q[203];
cz q[343], q[162];
cz q[344], q[237];
cz q[345], q[26];
cz q[346], q[41];
cz q[347], q[30];
cz q[348], q[51];
cz q[349], q[144];
cz q[350], q[201];
cz q[351], q[160];
cz q[352], q[235];
cz q[353], q[68];
cz q[354], q[97];
cz q[355], q[76];
cz q[356], q[115];
cz q[357], q[148];
cz q[358], q[205];
cz q[359], q[164];
cz q[360], q[239];
barrier q;

barrier q;

cx q[246], q[16];
cx q[247], q[18];
cx q[249], q[8];
cx q[252], q[13];
cx q[261], q[49];
cx q[262], q[52];
cx q[264], q[35];
cx q[267], q[44];
cx q[276], q[111];
cx q[277], q[116];
cx q[279], q[85];
cx q[282], q[102];
cx q[291], q[231];
cx q[292], q[240];
cx q[294], q[181];
cx q[297], q[214];
cz q[301], q[165];
cz q[302], q[141];
cz q[303], q[190];
cz q[304], q[182];
cz q[305], q[77];
cz q[306], q[65];
cz q[307], q[90];
cz q[308], q[86];
cz q[309], q[169];
cz q[310], q[145];
cz q[311], q[194];
cz q[312], q[186];
cz q[313], q[31];
cz q[314], q[25];
cz q[315], q[38];
cz q[316], q[36];
cz q[317], q[167];
cz q[318], q[143];
cz q[319], q[192];
cz q[320], q[184];
cz q[321], q[79];
cz q[322], q[67];
cz q[323], q[92];
cz q[324], q[88];
cz q[325], q[171];
cz q[326], q[147];
cz q[327], q[196];
cz q[328], q[188];
cz q[329], q[6];
cz q[330], q[3];
cz q[331], q[10];
cz q[332], q[9];
cz q[333], q[166];
cz q[334], q[142];
cz q[335], q[191];
cz q[336], q[183];
cz q[337], q[78];
cz q[338], q[66];
cz q[339], q[91];
cz q[340], q[87];
cz q[341], q[170];
cz q[342], q[146];
cz q[343], q[195];
cz q[344], q[187];
cz q[345], q[32];
cz q[346], q[26];
cz q[347], q[39];
cz q[348], q[37];
cz q[349], q[168];
cz q[350], q[144];
cz q[351], q[193];
cz q[352], q[185];
cz q[353], q[80];
cz q[354], q[68];
cz q[355], q[93];
cz q[356], q[89];
cz q[357], q[172];
cz q[358], q[148];
cz q[359], q[197];
cz q[360], q[189];
barrier q;

barrier q;

cx q[247], q[13];
cx q[253], q[8];
cx q[254], q[16];
cx q[255], q[18];
cx q[262], q[44];
cx q[268], q[35];
cx q[269], q[49];
cx q[270], q[52];
cx q[277], q[102];
cx q[283], q[85];
cx q[284], q[111];
cx q[285], q[116];
cx q[292], q[214];
cx q[298], q[181];
cx q[299], q[231];
cx q[300], q[240];
cz q[301], q[133];
cz q[302], q[182];
cz q[303], q[125];
cz q[304], q[117];
cz q[305], q[61];
cz q[306], q[86];
cz q[307], q[57];
cz q[308], q[53];
cz q[309], q[137];
cz q[310], q[186];
cz q[311], q[129];
cz q[312], q[121];
cz q[313], q[23];
cz q[314], q[36];
cz q[315], q[21];
cz q[316], q[19];
cz q[317], q[135];
cz q[318], q[184];
cz q[319], q[127];
cz q[320], q[119];
cz q[321], q[63];
cz q[322], q[88];
cz q[323], q[59];
cz q[324], q[55];
cz q[325], q[139];
cz q[326], q[188];
cz q[327], q[131];
cz q[328], q[123];
cz q[329], q[2];
cz q[330], q[9];
cz q[331], q[1];
cz q[332], q[0];
cz q[333], q[134];
cz q[334], q[183];
cz q[335], q[126];
cz q[336], q[118];
cz q[337], q[62];
cz q[338], q[87];
cz q[339], q[58];
cz q[340], q[54];
cz q[341], q[138];
cz q[342], q[187];
cz q[343], q[130];
cz q[344], q[122];
cz q[345], q[24];
cz q[346], q[37];
cz q[347], q[22];
cz q[348], q[20];
cz q[349], q[136];
cz q[350], q[185];
cz q[351], q[128];
cz q[352], q[120];
cz q[353], q[64];
cz q[354], q[89];
cz q[355], q[60];
cz q[356], q[56];
cz q[357], q[140];
cz q[358], q[189];
cz q[359], q[132];
cz q[360], q[124];
barrier q;

barrier q;

cx q[243], q[16];
cx q[249], q[18];
cx q[254], q[13];
cx q[255], q[8];
cx q[258], q[49];
cx q[264], q[52];
cx q[269], q[44];
cx q[270], q[35];
cx q[273], q[111];
cx q[279], q[116];
cx q[284], q[102];
cx q[285], q[85];
cx q[288], q[231];
cx q[294], q[240];
cx q[299], q[214];
cx q[300], q[181];
cz q[301], q[117];
cz q[302], q[125];
cz q[303], q[215];
cz q[304], q[165];
cz q[305], q[53];
cz q[306], q[57];
cz q[307], q[103];
cz q[308], q[77];
cz q[309], q[121];
cz q[310], q[129];
cz q[311], q[219];
cz q[312], q[169];
cz q[313], q[19];
cz q[314], q[21];
cz q[315], q[45];
cz q[316], q[31];
cz q[317], q[119];
cz q[318], q[127];
cz q[319], q[217];
cz q[320], q[167];
cz q[321], q[55];
cz q[322], q[59];
cz q[323], q[105];
cz q[324], q[79];
cz q[325], q[123];
cz q[326], q[131];
cz q[327], q[221];
cz q[328], q[171];
cz q[329], q[0];
cz q[330], q[1];
cz q[331], q[14];
cz q[332], q[6];
cz q[333], q[118];
cz q[334], q[126];
cz q[335], q[216];
cz q[336], q[166];
cz q[337], q[54];
cz q[338], q[58];
cz q[339], q[104];
cz q[340], q[78];
cz q[341], q[122];
cz q[342], q[130];
cz q[343], q[220];
cz q[344], q[170];
cz q[345], q[20];
cz q[346], q[22];
cz q[347], q[46];
cz q[348], q[32];
cz q[349], q[120];
cz q[350], q[128];
cz q[351], q[218];
cz q[352], q[168];
cz q[353], q[56];
cz q[354], q[60];
cz q[355], q[106];
cz q[356], q[80];
cz q[357], q[124];
cz q[358], q[132];
cz q[359], q[222];
cz q[360], q[172];
barrier q;

barrier q;

cx q[245], q[18];
cx q[246], q[13];
cx q[247], q[16];
cx q[251], q[8];
cx q[260], q[52];
cx q[261], q[44];
cx q[262], q[49];
cx q[266], q[35];
cx q[275], q[116];
cx q[276], q[102];
cx q[277], q[111];
cx q[281], q[85];
cx q[290], q[240];
cx q[291], q[214];
cx q[292], q[231];
cx q[296], q[181];
cz q[301], q[149];
cz q[302], q[190];
cz q[303], q[182];
cz q[304], q[198];
cz q[305], q[69];
cz q[306], q[90];
cz q[307], q[86];
cz q[308], q[94];
cz q[309], q[153];
cz q[310], q[194];
cz q[311], q[186];
cz q[312], q[202];
cz q[313], q[27];
cz q[314], q[38];
cz q[315], q[36];
cz q[316], q[40];
cz q[317], q[151];
cz q[318], q[192];
cz q[319], q[184];
cz q[320], q[200];
cz q[321], q[71];
cz q[322], q[92];
cz q[323], q[88];
cz q[324], q[96];
cz q[325], q[155];
cz q[326], q[196];
cz q[327], q[188];
cz q[328], q[204];
cz q[329], q[4];
cz q[330], q[10];
cz q[331], q[9];
cz q[332], q[11];
cz q[333], q[150];
cz q[334], q[191];
cz q[335], q[183];
cz q[336], q[199];
cz q[337], q[70];
cz q[338], q[91];
cz q[339], q[87];
cz q[340], q[95];
cz q[341], q[154];
cz q[342], q[195];
cz q[343], q[187];
cz q[344], q[203];
cz q[345], q[28];
cz q[346], q[39];
cz q[347], q[37];
cz q[348], q[41];
cz q[349], q[152];
cz q[350], q[193];
cz q[351], q[185];
cz q[352], q[201];
cz q[353], q[72];
cz q[354], q[93];
cz q[355], q[89];
cz q[356], q[97];
cz q[357], q[156];
cz q[358], q[197];
cz q[359], q[189];
cz q[360], q[205];
barrier q;

barrier q;

cx q[242], q[16];
cx q[243], q[18];
cx q[244], q[13];
cx q[254], q[8];
cx q[257], q[49];
cx q[258], q[52];
cx q[259], q[44];
cx q[269], q[35];
cx q[272], q[111];
cx q[273], q[116];
cx q[274], q[102];
cx q[284], q[85];
cx q[287], q[231];
cx q[288], q[240];
cx q[289], q[214];
cx q[299], q[181];
cz q[301], q[125];
cz q[302], q[206];
cz q[303], q[223];
cz q[304], q[215];
cz q[305], q[57];
cz q[306], q[98];
cz q[307], q[107];
cz q[308], q[103];
cz q[309], q[129];
cz q[310], q[210];
cz q[311], q[227];
cz q[312], q[219];
cz q[313], q[21];
cz q[314], q[42];
cz q[315], q[47];
cz q[316], q[45];
cz q[317], q[127];
cz q[318], q[208];
cz q[319], q[225];
cz q[320], q[217];
cz q[321], q[59];
cz q[322], q[100];
cz q[323], q[109];
cz q[324], q[105];
cz q[325], q[131];
cz q[326], q[212];
cz q[327], q[229];
cz q[328], q[221];
cz q[329], q[1];
cz q[330], q[12];
cz q[331], q[15];
cz q[332], q[14];
cz q[333], q[126];
cz q[334], q[207];
cz q[335], q[224];
cz q[336], q[216];
cz q[337], q[58];
cz q[338], q[99];
cz q[339], q[108];
cz q[340], q[104];
cz q[341], q[130];
cz q[342], q[211];
cz q[343], q[228];
cz q[344], q[220];
cz q[345], q[22];
cz q[346], q[43];
cz q[347], q[48];
cz q[348], q[46];
cz q[349], q[128];
cz q[350], q[209];
cz q[351], q[226];
cz q[352], q[218];
cz q[353], q[60];
cz q[354], q[101];
cz q[355], q[110];
cz q[356], q[106];
cz q[357], q[132];
cz q[358], q[213];
cz q[359], q[230];
cz q[360], q[222];
barrier q;

barrier q;

cz q[329], q[8];
cz q[330], q[13];
cz q[331], q[16];
cz q[332], q[18];
cz q[341], q[85];
cz q[342], q[102];
cz q[343], q[111];
cz q[344], q[116];
cz q[349], q[181];
cz q[350], q[214];
cz q[351], q[231];
cz q[352], q[240];
cz q[357], q[35];
cz q[358], q[44];
cz q[359], q[49];
cz q[360], q[52];
barrier q;

barrier q;

cx q[241], q[235];
cx q[242], q[226];
cx q[243], q[218];
cx q[244], q[209];
cx q[245], q[201];
cx q[246], q[193];
cx q[247], q[185];
cx q[248], q[176];
cx q[249], q[168];
cx q[250], q[160];
cx q[251], q[152];
cx q[252], q[144];
cx q[253], q[136];
cx q[254], q[128];
cx q[255], q[120];
cx q[256], q[238];
cx q[257], q[229];
cx q[258], q[221];
cx q[259], q[212];
cx q[260], q[204];
cx q[261], q[196];
cx q[262], q[188];
cx q[263], q[179];
cx q[264], q[171];
cx q[265], q[163];
cx q[266], q[155];
cx q[267], q[147];
cx q[268], q[139];
cx q[269], q[131];
cx q[270], q[123];
cx q[271], q[115];
cx q[272], q[110];
cx q[273], q[106];
cx q[274], q[101];
cx q[275], q[97];
cx q[276], q[93];
cx q[277], q[89];
cx q[278], q[84];
cx q[279], q[80];
cx q[280], q[76];
cx q[281], q[72];
cx q[282], q[68];
cx q[283], q[64];
cx q[284], q[60];
cx q[285], q[56];
cx q[286], q[239];
cx q[287], q[230];
cx q[288], q[222];
cx q[289], q[213];
cx q[290], q[205];
cx q[291], q[197];
cx q[292], q[189];
cx q[293], q[180];
cx q[294], q[172];
cx q[295], q[164];
cx q[296], q[156];
cx q[297], q[148];
cx q[298], q[140];
cx q[299], q[132];
cx q[300], q[124];
barrier q;

barrier q;

cz q[337], q[8];
cz q[338], q[13];
cz q[339], q[16];
cz q[340], q[18];
cz q[341], q[181];
cz q[342], q[214];
cz q[343], q[231];
cz q[344], q[240];
cz q[349], q[35];
cz q[350], q[44];
cz q[351], q[49];
cz q[352], q[52];
cz q[357], q[85];
cz q[358], q[102];
cz q[359], q[111];
cz q[360], q[116];
barrier q;

barrier q;

cx q[241], q[239];
cx q[242], q[230];
cx q[243], q[222];
cx q[244], q[213];
cx q[245], q[205];
cx q[246], q[197];
cx q[247], q[189];
cx q[248], q[180];
cx q[249], q[172];
cx q[250], q[164];
cx q[251], q[156];
cx q[252], q[148];
cx q[253], q[140];
cx q[254], q[132];
cx q[255], q[124];
cx q[256], q[115];
cx q[257], q[110];
cx q[258], q[106];
cx q[259], q[101];
cx q[260], q[97];
cx q[261], q[93];
cx q[262], q[89];
cx q[263], q[84];
cx q[264], q[80];
cx q[265], q[76];
cx q[266], q[72];
cx q[267], q[68];
cx q[268], q[64];
cx q[269], q[60];
cx q[270], q[56];
cx q[271], q[236];
cx q[272], q[227];
cx q[273], q[219];
cx q[274], q[210];
cx q[275], q[202];
cx q[276], q[194];
cx q[277], q[186];
cx q[278], q[177];
cx q[279], q[169];
cx q[280], q[161];
cx q[281], q[153];
cx q[282], q[145];
cx q[283], q[137];
cx q[284], q[129];
cx q[285], q[121];
cx q[286], q[233];
cx q[287], q[224];
cx q[288], q[216];
cx q[289], q[207];
cx q[290], q[199];
cx q[291], q[191];
cx q[292], q[183];
cx q[293], q[174];
cx q[294], q[166];
cx q[295], q[158];
cx q[296], q[150];
cx q[297], q[142];
cx q[298], q[134];
cx q[299], q[126];
cx q[300], q[118];
barrier q;

barrier q;

cz q[301], q[181];
cz q[302], q[214];
cz q[303], q[231];
cz q[304], q[240];
cz q[317], q[35];
cz q[318], q[44];
cz q[319], q[49];
cz q[320], q[52];
cz q[337], q[85];
cz q[338], q[102];
cz q[339], q[111];
cz q[340], q[116];
cz q[345], q[8];
cz q[346], q[13];
cz q[347], q[16];
cz q[348], q[18];
barrier q;

barrier q;

cx q[241], q[237];
cx q[242], q[228];
cx q[243], q[220];
cx q[244], q[211];
cx q[245], q[203];
cx q[246], q[195];
cx q[247], q[187];
cx q[248], q[178];
cx q[249], q[170];
cx q[250], q[162];
cx q[251], q[154];
cx q[252], q[146];
cx q[253], q[138];
cx q[254], q[130];
cx q[255], q[122];
cx q[256], q[114];
cx q[257], q[109];
cx q[258], q[105];
cx q[259], q[100];
cx q[260], q[96];
cx q[261], q[92];
cx q[262], q[88];
cx q[263], q[83];
cx q[264], q[79];
cx q[265], q[75];
cx q[266], q[71];
cx q[267], q[67];
cx q[268], q[63];
cx q[269], q[59];
cx q[270], q[55];
cx q[271], q[238];
cx q[272], q[229];
cx q[273], q[221];
cx q[274], q[212];
cx q[275], q[204];
cx q[276], q[196];
cx q[277], q[188];
cx q[278], q[179];
cx q[279], q[171];
cx q[280], q[163];
cx q[281], q[155];
cx q[282], q[147];
cx q[283], q[139];
cx q[284], q[131];
cx q[285], q[123];
cx q[286], q[234];
cx q[287], q[225];
cx q[288], q[217];
cx q[289], q[208];
cx q[290], q[200];
cx q[291], q[192];
cx q[292], q[184];
cx q[293], q[175];
cx q[294], q[167];
cx q[295], q[159];
cx q[296], q[151];
cx q[297], q[143];
cx q[298], q[135];
cx q[299], q[127];
cx q[300], q[119];
barrier q;

barrier q;

cz q[321], q[85];
cz q[322], q[102];
cz q[323], q[111];
cz q[324], q[116];
cz q[325], q[181];
cz q[326], q[214];
cz q[327], q[231];
cz q[328], q[240];
cz q[333], q[8];
cz q[334], q[13];
cz q[335], q[16];
cz q[336], q[18];
cz q[345], q[35];
cz q[346], q[44];
cz q[347], q[49];
cz q[348], q[52];
barrier q;

barrier q;

cx q[241], q[115];
cx q[242], q[110];
cx q[243], q[106];
cx q[244], q[101];
cx q[245], q[97];
cx q[246], q[93];
cx q[247], q[89];
cx q[248], q[84];
cx q[249], q[80];
cx q[250], q[76];
cx q[251], q[72];
cx q[252], q[68];
cx q[253], q[64];
cx q[254], q[60];
cx q[255], q[56];
cx q[256], q[50];
cx q[257], q[47];
cx q[258], q[45];
cx q[259], q[42];
cx q[260], q[40];
cx q[261], q[38];
cx q[262], q[36];
cx q[263], q[33];
cx q[264], q[31];
cx q[265], q[29];
cx q[266], q[27];
cx q[267], q[25];
cx q[268], q[23];
cx q[269], q[21];
cx q[270], q[19];
cx q[271], q[112];
cx q[272], q[107];
cx q[273], q[103];
cx q[274], q[98];
cx q[275], q[94];
cx q[276], q[90];
cx q[277], q[86];
cx q[278], q[81];
cx q[279], q[77];
cx q[280], q[73];
cx q[281], q[69];
cx q[282], q[65];
cx q[283], q[61];
cx q[284], q[57];
cx q[285], q[53];
cx q[286], q[236];
cx q[287], q[227];
cx q[288], q[219];
cx q[289], q[210];
cx q[290], q[202];
cx q[291], q[194];
cx q[292], q[186];
cx q[293], q[177];
cx q[294], q[169];
cx q[295], q[161];
cx q[296], q[153];
cx q[297], q[145];
cx q[298], q[137];
cx q[299], q[129];
cx q[300], q[121];
barrier q;

h q[241]; measure q[241] -> rec[0]; h q[241]; // decomposed MX
h q[242]; measure q[242] -> rec[1]; h q[242]; // decomposed MX
h q[243]; measure q[243] -> rec[2]; h q[243]; // decomposed MX
h q[244]; measure q[244] -> rec[3]; h q[244]; // decomposed MX
h q[245]; measure q[245] -> rec[4]; h q[245]; // decomposed MX
h q[246]; measure q[246] -> rec[5]; h q[246]; // decomposed MX
h q[247]; measure q[247] -> rec[6]; h q[247]; // decomposed MX
h q[248]; measure q[248] -> rec[7]; h q[248]; // decomposed MX
h q[249]; measure q[249] -> rec[8]; h q[249]; // decomposed MX
h q[250]; measure q[250] -> rec[9]; h q[250]; // decomposed MX
h q[251]; measure q[251] -> rec[10]; h q[251]; // decomposed MX
h q[252]; measure q[252] -> rec[11]; h q[252]; // decomposed MX
h q[253]; measure q[253] -> rec[12]; h q[253]; // decomposed MX
h q[254]; measure q[254] -> rec[13]; h q[254]; // decomposed MX
h q[255]; measure q[255] -> rec[14]; h q[255]; // decomposed MX
h q[256]; measure q[256] -> rec[15]; h q[256]; // decomposed MX
h q[257]; measure q[257] -> rec[16]; h q[257]; // decomposed MX
h q[258]; measure q[258] -> rec[17]; h q[258]; // decomposed MX
h q[259]; measure q[259] -> rec[18]; h q[259]; // decomposed MX
h q[260]; measure q[260] -> rec[19]; h q[260]; // decomposed MX
h q[261]; measure q[261] -> rec[20]; h q[261]; // decomposed MX
h q[262]; measure q[262] -> rec[21]; h q[262]; // decomposed MX
h q[263]; measure q[263] -> rec[22]; h q[263]; // decomposed MX
h q[264]; measure q[264] -> rec[23]; h q[264]; // decomposed MX
h q[265]; measure q[265] -> rec[24]; h q[265]; // decomposed MX
h q[266]; measure q[266] -> rec[25]; h q[266]; // decomposed MX
h q[267]; measure q[267] -> rec[26]; h q[267]; // decomposed MX
h q[268]; measure q[268] -> rec[27]; h q[268]; // decomposed MX
h q[269]; measure q[269] -> rec[28]; h q[269]; // decomposed MX
h q[270]; measure q[270] -> rec[29]; h q[270]; // decomposed MX
h q[271]; measure q[271] -> rec[30]; h q[271]; // decomposed MX
h q[272]; measure q[272] -> rec[31]; h q[272]; // decomposed MX
h q[273]; measure q[273] -> rec[32]; h q[273]; // decomposed MX
h q[274]; measure q[274] -> rec[33]; h q[274]; // decomposed MX
h q[275]; measure q[275] -> rec[34]; h q[275]; // decomposed MX
h q[276]; measure q[276] -> rec[35]; h q[276]; // decomposed MX
h q[277]; measure q[277] -> rec[36]; h q[277]; // decomposed MX
h q[278]; measure q[278] -> rec[37]; h q[278]; // decomposed MX
h q[279]; measure q[279] -> rec[38]; h q[279]; // decomposed MX
h q[280]; measure q[280] -> rec[39]; h q[280]; // decomposed MX
h q[281]; measure q[281] -> rec[40]; h q[281]; // decomposed MX
h q[282]; measure q[282] -> rec[41]; h q[282]; // decomposed MX
h q[283]; measure q[283] -> rec[42]; h q[283]; // decomposed MX
h q[284]; measure q[284] -> rec[43]; h q[284]; // decomposed MX
h q[285]; measure q[285] -> rec[44]; h q[285]; // decomposed MX
h q[286]; measure q[286] -> rec[45]; h q[286]; // decomposed MX
h q[287]; measure q[287] -> rec[46]; h q[287]; // decomposed MX
h q[288]; measure q[288] -> rec[47]; h q[288]; // decomposed MX
h q[289]; measure q[289] -> rec[48]; h q[289]; // decomposed MX
h q[290]; measure q[290] -> rec[49]; h q[290]; // decomposed MX
h q[291]; measure q[291] -> rec[50]; h q[291]; // decomposed MX
h q[292]; measure q[292] -> rec[51]; h q[292]; // decomposed MX
h q[293]; measure q[293] -> rec[52]; h q[293]; // decomposed MX
h q[294]; measure q[294] -> rec[53]; h q[294]; // decomposed MX
h q[295]; measure q[295] -> rec[54]; h q[295]; // decomposed MX
h q[296]; measure q[296] -> rec[55]; h q[296]; // decomposed MX
h q[297]; measure q[297] -> rec[56]; h q[297]; // decomposed MX
h q[298]; measure q[298] -> rec[57]; h q[298]; // decomposed MX
h q[299]; measure q[299] -> rec[58]; h q[299]; // decomposed MX
h q[300]; measure q[300] -> rec[59]; h q[300]; // decomposed MX
h q[301]; measure q[301] -> rec[60]; h q[301]; // decomposed MX
h q[302]; measure q[302] -> rec[61]; h q[302]; // decomposed MX
h q[303]; measure q[303] -> rec[62]; h q[303]; // decomposed MX
h q[304]; measure q[304] -> rec[63]; h q[304]; // decomposed MX
h q[305]; measure q[305] -> rec[64]; h q[305]; // decomposed MX
h q[306]; measure q[306] -> rec[65]; h q[306]; // decomposed MX
h q[307]; measure q[307] -> rec[66]; h q[307]; // decomposed MX
h q[308]; measure q[308] -> rec[67]; h q[308]; // decomposed MX
h q[309]; measure q[309] -> rec[68]; h q[309]; // decomposed MX
h q[310]; measure q[310] -> rec[69]; h q[310]; // decomposed MX
h q[311]; measure q[311] -> rec[70]; h q[311]; // decomposed MX
h q[312]; measure q[312] -> rec[71]; h q[312]; // decomposed MX
h q[313]; measure q[313] -> rec[72]; h q[313]; // decomposed MX
h q[314]; measure q[314] -> rec[73]; h q[314]; // decomposed MX
h q[315]; measure q[315] -> rec[74]; h q[315]; // decomposed MX
h q[316]; measure q[316] -> rec[75]; h q[316]; // decomposed MX
h q[317]; measure q[317] -> rec[76]; h q[317]; // decomposed MX
h q[318]; measure q[318] -> rec[77]; h q[318]; // decomposed MX
h q[319]; measure q[319] -> rec[78]; h q[319]; // decomposed MX
h q[320]; measure q[320] -> rec[79]; h q[320]; // decomposed MX
h q[321]; measure q[321] -> rec[80]; h q[321]; // decomposed MX
h q[322]; measure q[322] -> rec[81]; h q[322]; // decomposed MX
h q[323]; measure q[323] -> rec[82]; h q[323]; // decomposed MX
h q[324]; measure q[324] -> rec[83]; h q[324]; // decomposed MX
h q[325]; measure q[325] -> rec[84]; h q[325]; // decomposed MX
h q[326]; measure q[326] -> rec[85]; h q[326]; // decomposed MX
h q[327]; measure q[327] -> rec[86]; h q[327]; // decomposed MX
h q[328]; measure q[328] -> rec[87]; h q[328]; // decomposed MX
h q[329]; measure q[329] -> rec[88]; h q[329]; // decomposed MX
h q[330]; measure q[330] -> rec[89]; h q[330]; // decomposed MX
h q[331]; measure q[331] -> rec[90]; h q[331]; // decomposed MX
h q[332]; measure q[332] -> rec[91]; h q[332]; // decomposed MX
h q[333]; measure q[333] -> rec[92]; h q[333]; // decomposed MX
h q[334]; measure q[334] -> rec[93]; h q[334]; // decomposed MX
h q[335]; measure q[335] -> rec[94]; h q[335]; // decomposed MX
h q[336]; measure q[336] -> rec[95]; h q[336]; // decomposed MX
h q[337]; measure q[337] -> rec[96]; h q[337]; // decomposed MX
h q[338]; measure q[338] -> rec[97]; h q[338]; // decomposed MX
h q[339]; measure q[339] -> rec[98]; h q[339]; // decomposed MX
h q[340]; measure q[340] -> rec[99]; h q[340]; // decomposed MX
h q[341]; measure q[341] -> rec[100]; h q[341]; // decomposed MX
h q[342]; measure q[342] -> rec[101]; h q[342]; // decomposed MX
h q[343]; measure q[343] -> rec[102]; h q[343]; // decomposed MX
h q[344]; measure q[344] -> rec[103]; h q[344]; // decomposed MX
h q[345]; measure q[345] -> rec[104]; h q[345]; // decomposed MX
h q[346]; measure q[346] -> rec[105]; h q[346]; // decomposed MX
h q[347]; measure q[347] -> rec[106]; h q[347]; // decomposed MX
h q[348]; measure q[348] -> rec[107]; h q[348]; // decomposed MX
h q[349]; measure q[349] -> rec[108]; h q[349]; // decomposed MX
h q[350]; measure q[350] -> rec[109]; h q[350]; // decomposed MX
h q[351]; measure q[351] -> rec[110]; h q[351]; // decomposed MX
h q[352]; measure q[352] -> rec[111]; h q[352]; // decomposed MX
h q[353]; measure q[353] -> rec[112]; h q[353]; // decomposed MX
h q[354]; measure q[354] -> rec[113]; h q[354]; // decomposed MX
h q[355]; measure q[355] -> rec[114]; h q[355]; // decomposed MX
h q[356]; measure q[356] -> rec[115]; h q[356]; // decomposed MX
h q[357]; measure q[357] -> rec[116]; h q[357]; // decomposed MX
h q[358]; measure q[358] -> rec[117]; h q[358]; // decomposed MX
h q[359]; measure q[359] -> rec[118]; h q[359]; // decomposed MX
h q[360]; measure q[360] -> rec[119]; h q[360]; // decomposed MX
