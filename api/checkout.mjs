import {checkoutService} from '../lib/paypal.mjs';
export default async function handler(req,res){
 res.setHeader('Cache-Control','no-store');const send=(status,data)=>{res.statusCode=status;res.setHeader('Content-Type','application/json');res.end(JSON.stringify(data));};
 const service=checkoutService();if(req.method==='GET')return send(200,{sandbox:true,configured:service.configured()});
 if(req.method!=='POST')return send(405,{error:'POST required.'});
 if(!process.env.PUBLIC_ORIGIN||req.headers.origin!==new URL(process.env.PUBLIC_ORIGIN).origin)return send(403,{error:'Open the configured demo origin.'});
 try{const input=typeof req.body==='string'?JSON.parse(req.body):req.body;const cookies=Object.fromEntries((req.headers.cookie||'').split(';').filter(v=>v.includes('=')).map(v=>v.trim().split('=')));if(input?.action==='create'){const result=await service.create();res.setHeader('Set-Cookie','cif_checkout='+result.session+'; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=1800');return send(200,{approvalUrl:result.approvalUrl});}if(input?.action==='capture')return send(200,await service.capture(cookies.cif_checkout,input.orderId));return send(400,{error:'Unknown checkout action.'});}catch(error){return send(400,{error:error.message});}
}
