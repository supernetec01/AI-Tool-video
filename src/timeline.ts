export const FPS = 24;
export const TOTAL = 1440;
export const SHOTS = [
  {id:'hook',from:0,duration:120,title:'5 thực phẩm',tag:'DINH DƯỠNG MẸ BẦU',benefit:'hỗ trợ não bộ\nthai nhi',safety:'Ăn đa dạng · Chế biến an toàn',image:0,number:0},
  {id:'salmon',from:120,duration:192,title:'Cá hồi',tag:'DHA · OMEGA-3',benefit:'Hỗ trợ phát triển\nnão bộ và thị giác.',safety:'Chọn cá ít thủy ngân. Nấu chín.',image:1,number:1},
  {id:'egg',from:312,duration:192,title:'Trứng',tag:'CHOLINE',benefit:'Hỗ trợ phát triển\nnão và tủy sống.',safety:'Ăn trứng chín kỹ, cả lòng đỏ.',image:2,number:2},
  {id:'greens',from:504,duration:216,title:'Rau lá xanh',tag:'FOLATE',benefit:'Hỗ trợ hình thành\nống thần kinh thai nhi.',safety:'Folate trong rau không thay thế\naxit folic được khuyến nghị.',image:3,number:3},
  {id:'beef',from:720,duration:192,title:'Thịt bò nạc',tag:'SẮT',benefit:'Giúp vận chuyển oxy\nđến thai nhi.',safety:'Chế biến thịt chín kỹ.',image:4,number:4},
  {id:'dairy',from:912,duration:192,title:'Sữa & sữa chua',tag:'PROTEIN · I-ỐT',benefit:'Bổ sung dưỡng chất\ncho sự phát triển của bé.',safety:'Chọn sản phẩm thanh trùng\nhoặc tiệt trùng.',image:5,number:5},
  {id:'safe',from:1104,duration:216,title:'Bữa ăn cho mẹ,',tag:'ĂN ĐA DẠNG · AN TOÀN · ĐỦ CHẤT',benefit:'nền tảng cho bé.',safety:'Không có món ăn nào bảo đảm tăng IQ.',image:0,number:0},
  {id:'cta',from:1320,duration:120,title:'Lưu lại cho\nbữa ăn của mẹ.',tag:'MẸ BỈM THÔNG THÁI',benefit:'Theo dõi để xem thêm\nmẹo dinh dưỡng thai kỳ.',safety:'Bổ sung axit folic và vitamin bầu\ntheo hướng dẫn bác sĩ.',image:0,number:0},
] as const;
export type Shot = typeof SHOTS[number];
export const CAPTIONS = [
  {from:0,duration:120,text:'Mẹ bầu muốn con phát triển trí não khỏe mạnh? Lưu ngay 5 thực phẩm quen thuộc này nhé!'},
  {from:120,duration:192,text:'Thứ nhất, cá hồi. Giàu DHA, một dưỡng chất quan trọng cho sự phát triển não bộ và thị giác của bé.'},
  {from:312,duration:192,text:'Thứ hai, trứng. Chứa choline, hỗ trợ phát triển não và tủy sống của thai nhi. Mẹ nhớ ăn trứng chín kỹ.'},
  {from:504,duration:216,text:'Thứ ba, bông cải xanh và rau lá xanh. Cung cấp folate, hỗ trợ hình thành ống thần kinh. Rau không thay thế axit folic được khuyến nghị.'},
  {from:720,duration:192,text:'Thứ tư, thịt bò nạc. Cung cấp sắt, giúp vận chuyển oxy đến thai nhi. Mẹ nhớ chế biến thịt chín kỹ.'},
  {from:912,duration:192,text:'Cuối cùng, sữa và sữa chua. Bổ sung protein cùng các dưỡng chất như i-ốt. Chọn sản phẩm thanh trùng hoặc tiệt trùng.'},
  {from:1104,duration:216,text:'Mẹ nhớ ăn đa dạng, nấu chín thực phẩm và bổ sung vitamin bầu theo hướng dẫn bác sĩ. Không có món ăn nào bảo đảm tăng IQ.'},
  {from:1320,duration:120,text:'Lưu lại cho bữa ăn của mẹ! Bổ sung axit folic và vitamin bầu theo hướng dẫn bác sĩ.'},
];
export const SFX = SHOTS.slice(1).map(s=>({from:s.from,duration:16,src:'audio/soft-transition.wav',volume:0.12}));
