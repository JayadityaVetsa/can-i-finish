import path from 'node:path';
import {existsSync} from 'node:fs';
if(existsSync('.local/browsers'))process.env.PLAYWRIGHT_BROWSERS_PATH ||= path.resolve('.local/browsers');
const {createServer}=await import('./server.mjs');
const server=await createServer();console.log(`Can I Finish? Local runner: http://127.0.0.1:${server.address().port}`);
