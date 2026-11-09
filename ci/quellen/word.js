const fs=require('fs');
const {Document,Packer,Paragraph,TextRun,Header,Footer,ImageRun,AlignmentType,HorizontalPositionRelativeFrom,VerticalPositionRelativeFrom,TextWrappingType}=require('docx');
const mm=x=>Math.round(x*56.693);
const bg=f=>new Paragraph({children:[new ImageRun({type:'png',data:fs.readFileSync(f),transformation:{width:794,height:1123},
  floating:{horizontalPosition:{relative:HorizontalPositionRelativeFrom.PAGE,offset:0},verticalPosition:{relative:VerticalPositionRelativeFrom.PAGE,offset:0},behindDocument:true,allowOverlap:true,wrap:{type:TextWrappingType.NONE}},
  altText:{title:'Briefbogen',description:'Briefbogen Agentur Capeeshee',name:'Briefbogen'}})]});
const P=(t,o={})=>new Paragraph({spacing:{after:o.after??120,before:o.before??0,line:o.line??360},alignment:o.align,children:[new TextRun({text:t,font:o.font||'Poppins Light',size:o.size||20,bold:o.bold,color:o.color||'303133'})]});
const A=(t,o={})=>P(t,{font:'Poppins',line:276,after:0,...o});
const doc=new Document({
 creator:'Agentur Capeeshee',title:'Briefbogen Agentur Capeeshee',
 styles:{default:{document:{run:{font:'Poppins Light',size:20,color:'303133'},paragraph:{spacing:{line:360,after:120}}}}},
 sections:[{properties:{titlePage:true,page:{size:{width:11906,height:16838},margin:{top:mm(35),bottom:mm(36),left:mm(25),right:mm(20),header:mm(5),footer:mm(5)}}},
  headers:{first:new Header({children:[bg('brief-leer-300dpi.png')]}),default:new Header({children:[bg('brief-folge-300dpi.png')]})},
  footers:{first:new Footer({children:[new Paragraph({})]}),default:new Footer({children:[new Paragraph({})]})},
  children:[
   A('Firma',{before:mm(24.5)}),A('Frau Vorname Nachname'),A('Straße Hausnummer'),A('PLZ Ort'),
   P('Augsburg, TT. Monat JJJJ',{align:AlignmentType.RIGHT,before:mm(22),after:mm(8),color:'5F6164'}),
   P('Betreff',{font:'Poppins',bold:true,size:22,after:mm(6)}),
   P('Sehr geehrte Frau Nachname,'),
   P('hier beginnt Ihr Brieftext. Schreiben Sie einfach über diesen Platzhalter. Der Text läuft automatisch auf weitere Seiten, ab Seite 2 erscheint der Briefbogen ohne Siegel und Anschriftfeld.'),
   P('Mit freundlichen Grüßen',{before:120}),
   P('Alexander Windisch',{font:'Poppins',before:mm(10),after:0}),
   P('Agentur Capeeshee',{color:'5F6164'})
  ]}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync('Capeeshee-Briefvorlage.docx',b);console.log('ok')});
