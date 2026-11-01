const params=new URLSearchParams(location.search);const broken=params.get('version')!=='fixed';const journey=params.get('journey')||'registration';
const makeControl=(tag,id,text)=>{const n=document.createElement(tag);n.id=id;n.textContent=text;return n};
const register=makeControl(broken&&journey==='registration'?'div':'button','register','Register for Web Foundations');
if(register.tagName==='DIV'){register.setAttribute('role','button');register.className='faux';} // Deliberate fault: click-only control, absent from sequential focus.
register.onclick=()=>{document.getElementById('registration').hidden=false;document.getElementById('registration').scrollIntoView({block:'center'});};document.getElementById('register-slot').append(register);
document.getElementById('back').onclick=()=>{document.getElementById('registration').hidden=true;register.focus();};
const overlay=document.getElementById('overlay'),modal=document.getElementById('modal'),updates=document.getElementById('updates'),email=document.getElementById('email');
const close=makeControl(broken&&journey==='dialog'?'div':'button','close','Close updates');close.className=close.tagName==='DIV'?'faux':'';if(close.tagName==='DIV')close.setAttribute('role','button');document.getElementById('close-slot').append(close);
function dismiss(){overlay.hidden=true;updates.focus();}close.onclick=dismiss;
updates.onclick=()=>{overlay.hidden=false;email.focus();};document.getElementById('subscribe').onclick=()=>{document.getElementById('modal-note').textContent='Demo only: nothing was submitted.';};
document.addEventListener('keydown',event=>{if(overlay.hidden)return;if(event.key==='Escape'){event.preventDefault();if(!(broken&&journey==='dialog'))dismiss();return;}if(event.key==='Tab'){const focusables=[...modal.querySelectorAll('input,button')];const first=focusables[0],last=focusables.at(-1);if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}}});
