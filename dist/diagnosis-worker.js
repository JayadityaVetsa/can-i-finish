import {diagnosisMessages,validateDiagnosis,MODEL} from './diagnosis-core.js';
import {pipeline,env} from './vendor/transformers.js';
env.allowLocalModels=false;
env.backends.onnx.wasm.wasmPaths=new URL('./vendor/',self.location.href).href;
let generator;
self.onmessage=async({data})=>{try{
 if(!generator)generator=await pipeline('text-generation',MODEL,{revision:'774cc90',dtype:'q4f16',device:'webgpu',progress_callback:p=>self.postMessage({type:'progress',status:p.status,progress:p.progress})});
 const result=await generator(diagnosisMessages(data.input),{max_new_tokens:420,do_sample:false});
 const text=result[0].generated_text.at(-1).content;
 try{self.postMessage({type:'result',value:validateDiagnosis(text,data.input)});}catch(error){self.postMessage({type:'error',message:error.message,raw:text});}
 }catch(error){self.postMessage({type:'error',message:error.message});}};
