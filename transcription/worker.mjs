import { open, writeFile, mkdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

// Context overlaps by 5 seconds; accept words only from each unique 20-second core.
/** Keep words from a unique window core, clamp to audio bounds and discard invalid timing. */
export function selectWords(chunks, offset, coreStart, coreEnd, duration) {
  return (chunks ?? []).flatMap(chunk => {
    const [a,b] = chunk.timestamp ?? [];
    if (!Number.isFinite(a) || !Number.isFinite(b) || b <= a) return [];
    const start = Math.max(0, a+offset), end = Math.min(duration,b+offset);
    const middle = (start+end)/2;
    const text = String(chunk.text ?? '').replace(/[\x00-\x1f]+/g,' ').trim();
    return text && end>start && middle>=coreStart && middle<coreEnd ? [{start,end,text}] : [];
  });
}

/** Detect nontrivial RMS energy before spending CPU on a mostly silent window. */
export function audible(samples) {
  let sum=0; for (const value of samples) sum+=value*value;
  return samples.length && Math.sqrt(sum/samples.length)>=.001;
}

/** Read validated CLI options, run bounded local inference windows and emit JSON progress/results. */
async function main() {
  const [input,output,profile,language,cache,download] = process.argv.slice(2);
  if (!['tiny','base'].includes(profile) || !['auto','en','es','pt','fr','de','it'].includes(language))
    throw new Error('invalid-options');
  const emit = event => process.stdout.write(JSON.stringify(event)+'\n');
  const {pipeline,env} = await import('@huggingface/transformers');
  await mkdir(cache,{recursive:true});
  env.cacheDir=resolve(cache);
  env.allowRemoteModels=download==='true';
  env.allowLocalModels=true;
  env.remoteHost='https://huggingface.co';
  emit({phase:'loading_model'});
  const transcriber=await pipeline('automatic-speech-recognition',`Xenova/whisper-${profile}`,{
    device:'cpu',dtype:'q8',session_options:{intraOpNumThreads:2,interOpNumThreads:1},
  });
  const file=await open(input,'r');
  const duration=(await file.stat()).size/64000;
  const words=[];
  try {
    for(let core=0;core<duration;core+=20){
      const begin=Math.max(0,core-5), finish=Math.min(duration,core+25);
      const buffer=Buffer.alloc(Math.round((finish-begin)*16000)*4);
      const {bytesRead}=await file.read(buffer,0,buffer.length,Math.round(begin*16000)*4);
      const samples=new Float32Array(bytesRead/4);
      for(let i=0;i<samples.length;i++)samples[i]=buffer.readFloatLE(i*4);
      if(audible(samples)){
        const result=await transcriber(samples,{return_timestamps:'word',task:'transcribe',
          ...(language==='auto'?{}:{language})});
        const selected=selectWords(result.chunks,begin,core,Math.min(duration,core+20),duration);
        for(const word of selected){
          const previous=words.at(-1);
          if(previous && word.start<previous.end)word.start=previous.end;
          if(word.end>word.start)words.push(word);
        }
      }
      emit({phase:'transcribing',processed_seconds:Math.min(duration,core+20),duration});
    }
  } finally { await file.close(); await transcriber.dispose(); }
  if(!words.length)throw new Error('no-speech-or-timestamps');
  await writeFile(output,JSON.stringify({words}),'utf8');
  emit({phase:'complete'});
}

if(process.argv[1] && resolve(process.argv[1])===fileURLToPath(import.meta.url)){
  main().catch(()=>{process.stderr.write('local-transcription-failed\n');process.exitCode=1;});
}
