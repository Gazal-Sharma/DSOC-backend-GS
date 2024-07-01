(()=>{var Kn=Date.now(),oe=!("window"in globalThis)&&("serviceWorker"in globalThis||"registration"in globalThis&&"navigationPreload"in globalThis.registration),Ne="SW_VERSION_LOCAL",be="412ae0a6",ae="netlify-cnm",Ut="cnm-settings.json",Gt=`/${ae}/${Ut}`,Fn=(globalThis?.navigator?.userAgent||"").toLowerCase().includes("firefox"),Wt="cnm-sw.js",ce=`/${Wt}`,le="/cnm-main-client.js",$t="cnm.js",Pe=`/${ae}/${$t}`,Le="https://client-network-manager.netlify.app",Bn=`${Le}${ce}`,Vn=`${Le}${le}`;var xe=["1"];var Oe=1,he="__cnm-debug",ue="__cnm-settings",v="ntl-cnm-",Kt=1e3*60,Ft=1e3*10,Bt=1e3*60*60*4,Vt=["html","htm"],qt=["js","mjs"],jt=["css"],Yt=["svg","jpg","jpeg","gif","png","webp","avif","bmp","ico"],Xt=["tiff","tif","woff","woff2","ttf"],Jt=["aif","cda","mid","midi","mp3","mpa","wav","wma"],zt=["avi","mp4","mov"],qn=[...Vt,...qt,...jt,...Yt,...Xt,...Jt,...zt,"txt","pdf"];var De="disabled";var ge="enabled",ve="enabled",Me="disabled";var ke="disabled";var He="enforce";var Ue="cnm-sig-db-v1";var Ge="cnm-settings-v1";var We="cnm-hits-v1";var $e="api",Ke="config",Fe="lookahead";var Zt=1e3*60;var jn=1e3*60*60,Yn=1e3*60*60;var Qt="nomod",Xn=Qt.length;var Jn=`/${ae}/deltas/`;var L=!1,en="localStorage"in globalThis&&globalThis.document!==void 0,tn=en?`MAIN-${be}`:`SW-${Ne}`,Be=!1;function qe(){if(!Be){Be=!0;try{JSON.parse(localStorage.getItem("cnm-debug")||"")===!0&&(L=!0)}catch{}}}function fe(e){try{L!==!!e&&(L=!!e,L?localStorage.setItem("cnm-debug",JSON.stringify(L)):localStorage.removeItem("cnm-debug"))}catch{}}function je(){return fe(!L)}function de(){return location.href.includes(he)?!location.href.includes(`${he}=0`):null}function G(e,...t){L&&console[e](...t)}function W(e,t=90,n=80){let s=0;for(let i=0;i<e.length;i++)s=e.charCodeAt(i)+((s<<5)-s),s=s&s;return`hsl(${s%360}, ${t}%, ${n}%)`}var Ve=e=>{let t=`%cCNM ${tn} ::`;return e&&(t=`${t} ${e} ::`),{log:G.bind(null,"log",t,`background: ${e?W(e):"#bbb"}`),error:G.bind(null,"error",t,`background: ${e?W(e):"#bbb"}`),warn:G.bind(null,"warn",t,`background: ${e?W(e):"#bbb"}`),info:G.bind(null,"info",t,`background: ${e?W(e):"#bbb"}`),table:G.bind(null,"table",t,`background: ${e?W(e):"#bbb"}`)}},E={...Ve(),namespace:e=>({...Ve(e)})};function p(){let e=new URL(location.href),t=globalThis.netlify?.cnm?.settings;if(e.searchParams.has(ue)){let n=JSON.parse(e.searchParams.get(ue)||""),s={...t};return n?.clientCaching&&(s.clientCaching=n.clientCaching),n?.cachingOptions&&(s.cachingOptions=n.cachingOptions),n?.versionControls&&(s.versionControls={...s.versionControls,...n.versionControls}),n?.deltaEncoding&&(s.deltaEncoding=n.deltaEncoding),s}return t}function M(){return p()?.clientCaching!==De}var nn={},Ye=Date.now();function Xe(e){Ye=Date.now(),nn[e]=Ye}var K={},$=E.namespace("MSG-HANDLER"),Je=!1,pe,ze=null;oe&&self.addEventListener("message",e=>(Xe(e.type),Qe(e)));function Ze(e){$=E.namespace("MSG-HANDLER"),K=e.messageHandlers||{},pe=e.signalsManager,ze=e.beforeEach||null,e.messageListener&&!Je&&(Je=!0,e.messageListener.addEventListener("message",Qe))}function Qe(e){if(!e.data||!e.data.cnm)return;let{type:t,payload:n}=e.data,s=e.source;(ze?.()||Promise.resolve()).then(()=>{Object.keys(K).forEach(i=>{if(i===t||i.startsWith(`${t}_once_`)){let o=K[i];if(o)try{$.log(`start message handler for type "${t}"`);let l={type:t,payload:n,client:s};oe&&pe&&(l.serviceWorkerContext={signalsManager:pe}),o(l),$.log(`end message handler for type "${t}"`)}catch(l){$.error(`message handler for type "${t}" threw an error`),$.error(l)}i.includes("_once_")&&delete K[i]}})})}var sn=0;function et(e,t){K[`${e}_once_${sn}`]=t}function d(e,t={}){let n=navigator?.serviceWorker?.controller;n&&(M()||e==="SELF_DESTRUCT")&&n.postMessage({cnm:!0,type:e,payload:t})}var Z=!0;try{globalThis.localStorage.getItem("access_check__")}catch{Z=!1}var tt=e=>Z?globalThis.localStorage.getItem(e):void 0,nt=(e,t)=>Z?globalThis.localStorage.setItem(e,t):void 0,st=e=>Z?globalThis.localStorage.removeItem(e):void 0;function rt(e){return e.pathname.startsWith(ce)||e.pathname.startsWith(le)||e.pathname.startsWith(Pe)}var Q={},k=E.namespace("CACHE");function it(e){return e&&`${v}-${Oe}-${e}`}async function rn(e){k.log("start clearing caches",{signalKeys:e}),await Promise.allSettled(e.map(async t=>{let n="";typeof t=="object"?n=t.raw:typeof t=="string"&&(n=t),n&&(n=n.startsWith(v)?n:it(n),Q[n]||(Q[n]=await caches.open(n)),Q[n]&&(caches.delete(n),delete Q[n]))})),k.log("end clearing caches",{signalKeys:e})}async function on(e){k.log("start clearing all caches except these signals",{signalKeys:e});let t=await caches.keys(),n=e.map(({raw:i})=>it(i)),s=t.filter(i=>!n.includes(i)&&i.startsWith(v));s.length>0&&(k.log("keep cache keys",n),k.log("delete cache keys",s)),await rn(s),k.log("end clearing all other caches")}async function ot(){await on([])}var V=class{type=3;name="";prefix="";value="";suffix="";modifier=3;constructor(e,t,n,s,i,o){this.type=e,this.name=t,this.prefix=n,this.value=s,this.suffix=i,this.modifier=o}hasCustomName(){return this.name!==""&&typeof this.name!="number"}},an=/[$_\p{ID_Start}]/u,cn=/[$_\u200C\u200D\p{ID_Continue}]/u,me=".*";function ln(e,t){return(t?/^[\x00-\xFF]*$/:/^[\x00-\x7F]*$/).test(e)}function lt(e,t=!1){let n=[],s=0;for(;s<e.length;){let i=e[s],o=function(l){if(!t)throw new TypeError(l);n.push({type:"INVALID_CHAR",index:s,value:e[s++]})};if(i==="*"){n.push({type:"ASTERISK",index:s,value:e[s++]});continue}if(i==="+"||i==="?"){n.push({type:"OTHER_MODIFIER",index:s,value:e[s++]});continue}if(i==="\\"){n.push({type:"ESCAPED_CHAR",index:s++,value:e[s++]});continue}if(i==="{"){n.push({type:"OPEN",index:s,value:e[s++]});continue}if(i==="}"){n.push({type:"CLOSE",index:s,value:e[s++]});continue}if(i===":"){let l="",r=s+1;for(;r<e.length;){let c=e.substr(r,1);if(r===s+1&&an.test(c)||r!==s+1&&cn.test(c)){l+=e[r++];continue}break}if(!l){o(`Missing parameter name at ${s}`);continue}n.push({type:"NAME",index:s,value:l}),s=r;continue}if(i==="("){let l=1,r="",c=s+1,a=!1;if(e[c]==="?"){o(`Pattern cannot start with "?" at ${c}`);continue}for(;c<e.length;){if(!ln(e[c],!1)){o(`Invalid character '${e[c]}' at ${c}.`),a=!0;break}if(e[c]==="\\"){r+=e[c++]+e[c++];continue}if(e[c]===")"){if(l--,l===0){c++;break}}else if(e[c]==="("&&(l++,e[c+1]!=="?")){o(`Capturing groups are not allowed at ${c}`),a=!0;break}r+=e[c++]}if(a)continue;if(l){o(`Unbalanced pattern at ${s}`);continue}if(!r){o(`Missing pattern at ${s}`);continue}n.push({type:"REGEX",index:s,value:r}),s=c;continue}n.push({type:"CHAR",index:s,value:e[s++]})}return n.push({type:"END",index:s,value:""}),n}function ht(e,t={}){let n=lt(e);t.delimiter??="/#?",t.prefixes??="./";let s=`[^${_(t.delimiter)}]+?`,i=[],o=0,l=0,r="",c=new Set,a=f=>{if(l<n.length&&n[l].type===f)return n[l++].value},u=()=>a("OTHER_MODIFIER")??a("ASTERISK"),h=f=>{let S=a(f);if(S!==void 0)return S;let{type:m,index:D}=n[l];throw new TypeError(`Unexpected ${m} at ${D}, expected ${f}`)},g=()=>{let f="",S;for(;S=a("CHAR")??a("ESCAPED_CHAR");)f+=S;return f},X=f=>f,J=t.encodePart||X,z="",re=f=>{z+=f},ie=()=>{z.length&&(i.push(new V(3,"","",J(z),"",3)),z="")},we=(f,S,m,D,w)=>{let R=3;switch(w){case"?":R=1;break;case"*":R=0;break;case"+":R=2;break}if(!S&&!m&&R===3){re(f);return}if(ie(),!S&&!m){if(!f)return;i.push(new V(3,"","",J(f),"",R));return}let C;m?m==="*"?C=me:C=m:C=s;let U=2;C===s?(U=1,C=""):C===me&&(U=0,C="");let N;if(S?N=S:m&&(N=o++),c.has(N))throw new TypeError(`Duplicate name '${N}'.`);c.add(N),i.push(new V(U,N,J(f),C,J(D),R))};for(;l<n.length;){let f=a("CHAR"),S=a("NAME"),m=a("REGEX");if(!S&&!m&&(m=a("ASTERISK")),S||m){let w=f??"";t.prefixes.indexOf(w)===-1&&(re(w),w=""),ie();let R=u();we(w,S,m,"",R);continue}let D=f??a("ESCAPED_CHAR");if(D){re(D);continue}if(a("OPEN")){let w=g(),R=a("NAME"),C=a("REGEX");!R&&!C&&(C=a("ASTERISK"));let U=g();h("CLOSE");let N=u();we(w,R,C,U,N);continue}ie(),h("END")}return i}function _(e){return e.replace(/([.+*?^${}()[\]|/\\])/g,"\\$1")}function at(e){return e&&e.ignoreCase?"ui":"u"}function hn(e,t,n){return ut(ht(e,n),t,n)}function H(e){switch(e){case 0:return"*";case 1:return"?";case 2:return"+";case 3:return""}}function ut(e,t,n={}){n.delimiter??="/#?",n.prefixes??="./",n.sensitive??=!1,n.strict??=!1,n.end??=!0,n.start??=!0,n.endsWith="";let s=n.start?"^":"";for(let r of e){if(r.type===3){r.modifier===3?s+=_(r.value):s+=`(?:${_(r.value)})${H(r.modifier)}`;continue}t&&t.push(r.name);let c=`[^${_(n.delimiter)}]+?`,a=r.value;if(r.type===1?a=c:r.type===0&&(a=me),!r.prefix.length&&!r.suffix.length){r.modifier===3||r.modifier===1?s+=`(${a})${H(r.modifier)}`:s+=`((?:${a})${H(r.modifier)})`;continue}if(r.modifier===3||r.modifier===1){s+=`(?:${_(r.prefix)}(${a})${_(r.suffix)})`,s+=H(r.modifier);continue}s+=`(?:${_(r.prefix)}`,s+=`((?:${a})(?:`,s+=_(r.suffix),s+=_(r.prefix),s+=`(?:${a}))*)${_(r.suffix)})`,r.modifier===0&&(s+="?")}let i=`[${_(n.endsWith)}]|$`,o=`[${_(n.delimiter)}]`;if(n.end)return n.strict||(s+=`${o}?`),n.endsWith.length?s+=`(?=${i})`:s+="$",new RegExp(s,at(n));n.strict||(s+=`(?:${o}(?=${i}))?`);let l=!1;if(e.length){let r=e[e.length-1];r.type===3&&r.modifier===3&&(l=n.delimiter.indexOf(r)>-1)}return l||(s+=`(?=${o}|${i})`),new RegExp(s,at(n))}var P={delimiter:"",prefixes:"",sensitive:!0,strict:!0},un={delimiter:".",prefixes:"",sensitive:!0,strict:!0},gn={delimiter:"/",prefixes:"/",sensitive:!0,strict:!0};function fn(e,t){return e.length?e[0]==="/"?!0:!t||e.length<2?!1:(e[0]=="\\"||e[0]=="{")&&e[1]=="/":!1}function gt(e,t){return e.startsWith(t)?e.substring(t.length,e.length):e}function dn(e,t){return e.endsWith(t)?e.substr(0,e.length-t.length):e}function ft(e){return!e||e.length<2?!1:e[0]==="["||(e[0]==="\\"||e[0]==="{")&&e[1]==="["}var dt=["ftp","file","http","https","ws","wss"];function pt(e){if(!e)return!0;for(let t of dt)if(e.test(t))return!0;return!1}function pn(e,t){if(e=gt(e,"#"),t||e==="")return e;let n=new URL("https://example.com");return n.hash=e,n.hash?n.hash.substring(1,n.hash.length):""}function Sn(e,t){if(e=gt(e,"?"),t||e==="")return e;let n=new URL("https://example.com");return n.search=e,n.search?n.search.substring(1,n.search.length):""}function mn(e,t){return t||e===""?e:ft(e)?Et(e):mt(e)}function En(e,t){if(t||e==="")return e;let n=new URL("https://example.com");return n.password=e,n.password}function Cn(e,t){if(t||e==="")return e;let n=new URL("https://example.com");return n.username=e,n.username}function _n(e,t,n){if(n||e==="")return e;if(t&&!dt.includes(t))return new URL(`${t}:${e}`).pathname;let s=e[0]=="/";return e=new URL(s?e:"/-"+e,"https://example.com").pathname,s||(e=e.substring(2,e.length)),e}function Tn(e,t,n){return St(t)===e&&(e=""),n||e===""?e:Ct(e)}function Rn(e,t){return e=dn(e,":"),t||e===""?e:Ee(e)}function St(e){switch(e){case"ws":case"http":return"80";case"wws":case"https":return"443";case"ftp":return"21";default:return""}}function Ee(e){if(e==="")return e;if(/^[-+.A-Za-z0-9]*$/.test(e))return e.toLowerCase();throw new TypeError(`Invalid protocol '${e}'.`)}function In(e){if(e==="")return e;let t=new URL("https://example.com");return t.username=e,t.username}function yn(e){if(e==="")return e;let t=new URL("https://example.com");return t.password=e,t.password}function mt(e){if(e==="")return e;if(/[\t\n\r #%/:<>?@[\]^\\|]/g.test(e))throw new TypeError(`Invalid hostname '${e}'`);let t=new URL("https://example.com");return t.hostname=e,t.hostname}function Et(e){if(e==="")return e;if(/[^0-9a-fA-F[\]:]/g.test(e))throw new TypeError(`Invalid IPv6 hostname '${e}'`);return e.toLowerCase()}function Ct(e){if(e===""||/^[0-9]*$/.test(e)&&parseInt(e)<=65535)return e;throw new TypeError(`Invalid port '${e}'.`)}function An(e){if(e==="")return e;let t=new URL("https://example.com");return t.pathname=e[0]!=="/"?"/-"+e:e,e[0]!=="/"?t.pathname.substring(2,t.pathname.length):t.pathname}function wn(e){return e===""?e:new URL(`data:${e}`).pathname}function Nn(e){if(e==="")return e;let t=new URL("https://example.com");return t.search=e,t.search.substring(1,t.search.length)}function bn(e){if(e==="")return e;let t=new URL("https://example.com");return t.hash=e,t.hash.substring(1,t.hash.length)}var Pn=class{#i;#s=[];#t={};#e=0;#r=1;#g=0;#c=0;#f=0;#d=0;#p=!1;constructor(e){this.#i=e}get result(){return this.#t}parse(){for(this.#s=lt(this.#i,!0);this.#e<this.#s.length;this.#e+=this.#r){if(this.#r=1,this.#s[this.#e].type==="END"){if(this.#c===0){this.#C(),this.#l()?this.#n(9,1):this.#h()?(this.#n(8,1),this.#t.hash=""):(this.#n(7,0),this.#t.search="",this.#t.hash="");continue}else if(this.#c===2){this.#u(5);continue}this.#n(10,0);break}if(this.#f>0)if(this.#w())this.#f-=1;else continue;if(this.#A()){this.#f+=1;continue}switch(this.#c){case 0:this.#_()&&(this.#t.username="",this.#t.password="",this.#t.hostname="",this.#t.port="",this.#t.pathname="",this.#t.search="",this.#t.hash="",this.#u(1));break;case 1:if(this.#_()){this.#P();let e=7,t=1;this.#p&&(this.#t.pathname="/"),this.#R()?(e=2,t=3):this.#p&&(e=2),this.#n(e,t)}break;case 2:this.#m()?this.#u(3):(this.#E()||this.#h()||this.#l())&&this.#u(5);break;case 3:this.#I()?this.#n(4,1):this.#m()&&this.#n(5,1);break;case 4:this.#m()&&this.#n(5,1);break;case 5:this.#N()?this.#d+=1:this.#b()&&(this.#d-=1),this.#y()&&!this.#d?this.#n(6,1):this.#E()?this.#n(7,0):this.#h()?this.#n(8,1):this.#l()&&this.#n(9,1);break;case 6:this.#E()?this.#n(7,0):this.#h()?this.#n(8,1):this.#l()&&this.#n(9,1);break;case 7:this.#h()?this.#n(8,1):this.#l()&&this.#n(9,1);break;case 8:this.#l()&&this.#n(9,1);break;case 9:break;case 10:break}}}#n(e,t){switch(this.#c){case 0:break;case 1:this.#t.protocol=this.#a();break;case 2:break;case 3:this.#t.username=this.#a();break;case 4:this.#t.password=this.#a();break;case 5:this.#t.hostname=this.#a();break;case 6:this.#t.port=this.#a();break;case 7:this.#t.pathname=this.#a();break;case 8:this.#t.search=this.#a();break;case 9:this.#t.hash=this.#a();break;case 10:break}this.#T(e,t)}#T(e,t){this.#c=e,this.#g=this.#e+t,this.#e+=t,this.#r=0}#C(){this.#e=this.#g,this.#r=0}#u(e){this.#C(),this.#c=e}#S(e){return e<0&&(e=this.#s.length-e),e<this.#s.length?this.#s[e]:this.#s[this.#s.length-1]}#o(e,t){let n=this.#S(e);return n.value===t&&(n.type==="CHAR"||n.type==="ESCAPED_CHAR"||n.type==="INVALID_CHAR")}#_(){return this.#o(this.#e,":")}#R(){return this.#o(this.#e+1,"/")&&this.#o(this.#e+2,"/")}#m(){return this.#o(this.#e,"@")}#I(){return this.#o(this.#e,":")}#y(){return this.#o(this.#e,":")}#E(){return this.#o(this.#e,"/")}#h(){if(this.#o(this.#e,"?"))return!0;if(this.#s[this.#e].value!=="?")return!1;let e=this.#S(this.#e-1);return e.type!=="NAME"&&e.type!=="REGEX"&&e.type!=="CLOSE"&&e.type!=="ASTERISK"}#l(){return this.#o(this.#e,"#")}#A(){return this.#s[this.#e].type=="OPEN"}#w(){return this.#s[this.#e].type=="CLOSE"}#N(){return this.#o(this.#e,"[")}#b(){return this.#o(this.#e,"]")}#a(){let e=this.#s[this.#e],t=this.#S(this.#g).index;return this.#i.substring(t,e.index)}#P(){let e={};Object.assign(e,P),e.encodePart=Ee;let t=hn(this.#a(),void 0,e);this.#p=pt(t)}},Se=["protocol","username","password","hostname","port","pathname","search","hash"],b="*";function ct(e,t){if(typeof e!="string")throw new TypeError("parameter 1 is not of type 'string'.");let n=new URL(e,t);return{protocol:n.protocol.substring(0,n.protocol.length-1),username:n.username,password:n.password,hostname:n.hostname,port:n.port,pathname:n.pathname,search:n.search!==""?n.search.substring(1,n.search.length):void 0,hash:n.hash!==""?n.hash.substring(1,n.hash.length):void 0}}function I(e,t){return t?B(e):e}function F(e,t,n){let s;if(typeof t.baseURL=="string")try{s=new URL(t.baseURL),e.protocol=I(s.protocol.substring(0,s.protocol.length-1),n),e.username=I(s.username,n),e.password=I(s.password,n),e.hostname=I(s.hostname,n),e.port=I(s.port,n),e.pathname=I(s.pathname,n),e.search=I(s.search.substring(1,s.search.length),n),e.hash=I(s.hash.substring(1,s.hash.length),n)}catch{throw new TypeError(`invalid baseURL '${t.baseURL}'.`)}if(typeof t.protocol=="string"&&(e.protocol=Rn(t.protocol,n)),typeof t.username=="string"&&(e.username=Cn(t.username,n)),typeof t.password=="string"&&(e.password=En(t.password,n)),typeof t.hostname=="string"&&(e.hostname=mn(t.hostname,n)),typeof t.port=="string"&&(e.port=Tn(t.port,e.protocol,n)),typeof t.pathname=="string"){if(e.pathname=t.pathname,s&&!fn(e.pathname,n)){let i=s.pathname.lastIndexOf("/");i>=0&&(e.pathname=I(s.pathname.substring(0,i+1),n)+e.pathname)}e.pathname=_n(e.pathname,e.protocol,n)}return typeof t.search=="string"&&(e.search=Sn(t.search,n)),typeof t.hash=="string"&&(e.hash=pn(t.hash,n)),e}function B(e){return e.replace(/([+*?:{}()\\])/g,"\\$1")}function Ln(e){return e.replace(/([.+*?^${}()[\]|/\\])/g,"\\$1")}function xn(e,t){t.delimiter??="/#?",t.prefixes??="./",t.sensitive??=!1,t.strict??=!1,t.end??=!0,t.start??=!0,t.endsWith="";let n=".*",s=`[^${Ln(t.delimiter)}]+?`,i=/[$_\u200C\u200D\p{ID_Continue}]/u,o="";for(let l=0;l<e.length;++l){let r=e[l];if(r.type===3){if(r.modifier===3){o+=B(r.value);continue}o+=`{${B(r.value)}}${H(r.modifier)}`;continue}let c=r.hasCustomName(),a=!!r.suffix.length||!!r.prefix.length&&(r.prefix.length!==1||!t.prefixes.includes(r.prefix)),u=l>0?e[l-1]:null,h=l<e.length-1?e[l+1]:null;if(!a&&c&&r.type===1&&r.modifier===3&&h&&!h.prefix.length&&!h.suffix.length)if(h.type===3){let g=h.value.length>0?h.value[0]:"";a=i.test(g)}else a=!h.hasCustomName();if(!a&&!r.prefix.length&&u&&u.type===3){let g=u.value[u.value.length-1];a=t.prefixes.includes(g)}a&&(o+="{"),o+=B(r.prefix),c&&(o+=`:${r.name}`),r.type===2?o+=`(${r.value})`:r.type===1?c||(o+=`(${s})`):r.type===0&&(!c&&(!u||u.type===3||u.modifier!==3||a||r.prefix!=="")?o+="*":o+=`(${n})`),r.type===1&&c&&r.suffix.length&&i.test(r.suffix[0])&&(o+="\\"),o+=B(r.suffix),a&&(o+="}"),r.modifier!==3&&(o+=H(r.modifier))}return o}var q=class{#i;#s={};#t={};#e={};#r={};constructor(e={},t,n){try{let s;if(typeof t=="string"?s=t:n=t,typeof e=="string"){let r=new Pn(e);if(r.parse(),e=r.result,s===void 0&&typeof e.protocol!="string")throw new TypeError("A base URL must be provided for a relative constructor string.");e.baseURL=s}else{if(!e||typeof e!="object")throw new TypeError("parameter 1 is not of type 'string' and cannot convert to dictionary.");if(s)throw new TypeError("parameter 1 is not of type 'string'.")}typeof n>"u"&&(n={ignoreCase:!1});let i={ignoreCase:n.ignoreCase===!0},o={pathname:b,protocol:b,username:b,password:b,hostname:b,port:b,search:b,hash:b};this.#i=F(o,e,!0),St(this.#i.protocol)===this.#i.port&&(this.#i.port="");let l;for(l of Se){if(!(l in this.#i))continue;let r={},c=this.#i[l];switch(this.#t[l]=[],l){case"protocol":Object.assign(r,P),r.encodePart=Ee;break;case"username":Object.assign(r,P),r.encodePart=In;break;case"password":Object.assign(r,P),r.encodePart=yn;break;case"hostname":Object.assign(r,un),ft(c)?r.encodePart=Et:r.encodePart=mt;break;case"port":Object.assign(r,P),r.encodePart=Ct;break;case"pathname":pt(this.#s.protocol)?(Object.assign(r,gn,i),r.encodePart=An):(Object.assign(r,P,i),r.encodePart=wn);break;case"search":Object.assign(r,P,i),r.encodePart=Nn;break;case"hash":Object.assign(r,P,i),r.encodePart=bn;break}try{this.#r[l]=ht(c,r),this.#s[l]=ut(this.#r[l],this.#t[l],r),this.#e[l]=xn(this.#r[l],r)}catch{throw new TypeError(`invalid ${l} pattern '${this.#i[l]}'.`)}}}catch(s){throw new TypeError(`Failed to construct 'URLPattern': ${s.message}`)}}test(e={},t){let n={pathname:"",protocol:"",username:"",password:"",hostname:"",port:"",search:"",hash:""};if(typeof e!="string"&&t)throw new TypeError("parameter 1 is not of type 'string'.");if(typeof e>"u")return!1;try{typeof e=="object"?n=F(n,e,!1):n=F(n,ct(e,t),!1)}catch{return!1}let s;for(s of Se)if(!this.#s[s].exec(n[s]))return!1;return!0}exec(e={},t){let n={pathname:"",protocol:"",username:"",password:"",hostname:"",port:"",search:"",hash:""};if(typeof e!="string"&&t)throw new TypeError("parameter 1 is not of type 'string'.");if(typeof e>"u")return;try{typeof e=="object"?n=F(n,e,!1):n=F(n,ct(e,t),!1)}catch{return null}let s={};t?s.inputs=[e,t]:s.inputs=[e];let i;for(i of Se){let o=this.#s[i].exec(n[i]);if(!o)return null;let l={};for(let[r,c]of this.#t[i].entries())if(typeof c=="string"||typeof c=="number"){let a=o[r+1];l[c]=a}s[i]={input:n[i]??"",groups:l}}return s}static compareComponent(e,t,n){let s=(r,c)=>{for(let a of["type","modifier","prefix","value","suffix"]){if(r[a]<c[a])return-1;if(r[a]!==c[a])return 1}return 0},i=new V(3,"","","","",3),o=new V(0,"","","","",3),l=(r,c)=>{let a=0;for(;a<Math.min(r.length,c.length);++a){let u=s(r[a],c[a]);if(u)return u}return r.length===c.length?0:s(r[a]??i,c[a]??i)};return!t.#e[e]&&!n.#e[e]?0:t.#e[e]&&!n.#e[e]?l(t.#r[e],[o]):!t.#e[e]&&n.#e[e]?l([o],n.#r[e]):l(t.#r[e],n.#r[e])}get protocol(){return this.#e.protocol}get username(){return this.#e.username}get password(){return this.#e.password}get hostname(){return this.#e.hostname}get port(){return this.#e.port}get pathname(){return this.#e.pathname}get search(){return this.#e.search}get hash(){return this.#e.hash}};globalThis.URLPattern||(globalThis.URLPattern=q);var ee=!0;try{globalThis.sessionStorage.getItem("access_check__")}catch{ee=!1}var Ce=e=>ee?globalThis.sessionStorage.getItem(e):void 0,_e=(e,t)=>ee?globalThis.sessionStorage.setItem(e,t):void 0,_t=e=>ee?globalThis.sessionStorage.removeItem(e):void 0;function Tt(e){let t=[],n=e.split(";");return n.forEach(s=>{if(s)if(s.includes(":")){let[i,o]=s.split(":");i?.trim()&&o?.trim()&&t.push({version:i.trim(),pattern:o.trim()})}else n.length===1&&t.push({version:s,pattern:"/*"})}),t}function On(e,t,n){if(e===t)return!0;if(e&&!t||t&&!e||!t&&!e)return!1;let s=new URL(n.href),i=Tt(e),o=Tt(t),l=[],r=[];if(i.forEach(({pattern:u,version:h})=>{new q({pathname:u,search:"*",hash:"*",baseURL:s.origin}).test(n.href)&&r.push(h)}),o.forEach(({pattern:u,version:h})=>{new q({pathname:u,search:"*",hash:"*",baseURL:s.origin}).test(n.href)&&l.push(h)}),l.length!==r.length)return!1;let c=[...r],a=!1;return l.forEach(u=>{let h=c.indexOf(u);h>-1?c.splice(h,1):a=!0}),!(a||c.length>0)}var Te=[];function Rt(e,t,n,s,i){if(n&&Te.length>0&&n.raw!==e.raw){let o=i===He&&!On(t,s,window.location),l=Te.reduce((r,c)=>{try{let a=c({currentDeployId:e.deployId,currentDeployBuildUTC:e.buildUTC,latestDeployId:n.deployId,latestDeployBuildUTC:n.buildUTC,forcingReload:o});!r&&a===!1&&(r=!0)}catch(a){console.error(a)}return r},!1);if(o&&!l){let r=JSON.parse(Ce("cnm_reload")||"{}"),c=r?.forcedReloadsCount||0;if(r?.lastForceReload){if(Date.now()-r.lastForceReload<=6e4&&c>=3)return;c=0}_e("cnm_reload_state",JSON.stringify({lastForceReload:Date.now(),forcedReloadsCount:++c})),_e("cnm_reload_user_state",JSON.stringify({scrollX:window.scrollX,scrollY:window.scrollY})),window.location.reload()}}}function It(e){Te.push(e)}function yt(){let e=JSON.parse(Ce("cnm_reload_user_state")||"{}");e?.scrollX&&(window.scrollX=e.scrollX),e?.scrollY&&(window.scrollY=e.scrollY),"scrollY"in e&&_t("cnm_reload_user_state")}var vn=E.namespace("SIGNALS-MANAGER");function At(e){if(!e)return;let[t,n,s,i]=e.split(":"),o=parseInt(i||"0");if(!t||!xe.includes(t)||!n||!s||!o){vn.error("invalid signal keys are being deconstructed",e);return}return{keyVersion:t,siteId:n,deployId:s,buildUTC:o,raw:e}}function wt(){if(p().cachingOptions?.precachingLookahead===Me)return;let e=[];document.querySelectorAll("img[loading=lazy]").forEach(t=>{"complete"in t&&!t.complete&&("currentSrc"in t&&t.currentSrc?e.push({url:t.currentSrc,destination:"image"}):"src"in t&&t.src?e.push({url:t.src,destination:"image"}):"href"in t&&t.href&&e.push({url:t.href,destination:"image"}))}),e.length>0&&te(e,Fe)}function te(e,t){d("PRECACHE_RESOURCES",{resources:e,src:t})}var Nt=({payload:e})=>{if(p().cachingOptions?.precachingLookahead===ve&&e&&typeof e.maxPrecache=="number"){let{maxPrecache:n}=e,s=0;document.querySelectorAll("img[loading=lazy]").forEach(i=>{"complete"in i&&!i.complete&&"loading"in i&&s<=n&&(i.loading="eager",s++)})}},bt=()=>{let e=p().cachingOptions?.precachingConfiguredRoutes;Array.isArray(e)&&e.length>0&&te(e.map(t=>({url:t})),Ke)};function x(e,t,n){let s=e.length;if(!s)return;if(n=Object.prototype.toString.call(n)=="[object Function]"?n:function(c){return c},t=+t,t<=0||s<2)return+n(e[0],0,e);if(t>=1)return+n(e[s-1],s-1,e);let i=(s-1)*t,o=Math.floor(i),l=+n(e[o],o,e),r=+n(e[o+1],o+1,e);return l+(r-l)*(i-o)}var y=self.location.origin,Mn=self.location.hostname,kn=Mn==="netlify.com"||y.endsWith(".netlify.com")||y.endsWith("--app.netlify.app")||y.endsWith("--docs.netlify.app")||y.endsWith("--www.netlify.app")||y.endsWith("--app.netlify.com")||y.endsWith("--www.netlify.com")||y.endsWith("--docs.netlify.com"),Hn=y.endsWith("--client-network-manager.netlify.app")||y.endsWith("client-network-manager.netlify.app"),j=E.namespace("rum-reporter");function ne(){return kn&&"DD_RUM"in window||Hn}function O(e,t){j.log("RUM log:",e,t),ne()&&"DD_RUM"in window&&window.DD_RUM.addAction(e,t)}function Y(e,t){j.log("RUM global context:",e,t),ne()&&"DD_RUM"in window&&("setGlobalContextProperty"in window.DD_RUM?window.DD_RUM.setGlobalContextProperty(e,t):"addRumGlobalContext"in window.DD_RUM&&window.DD_RUM.addRumGlobalContext(e,t))}var Pt={meta:{},stats:{},races:[],deltaResponses:[]},T={...Pt};async function Un(e="unknown"){if(document.visibilityState==="hidden"||!ne())return;let t=await Promise.race([window.netlify?.cnm?.getStats?.(),new Promise(a=>{setTimeout(()=>{a(null)},1e3)})]);if(!t||typeof t!="object"||!("stats"in t))return;let n=t,s=!!(n&&"meta"in n)&&typeof n.stats=="object",i=T?.meta?.version;n.meta.version&&i&&i!==n.meta.version&&(T={...Pt});let o=!!(T&&"meta"in T)&&typeof T.stats=="object",l=s&&o?Object.keys(n.stats).reduce((a,u)=>(isNaN(n.stats[u])||isNaN(T.stats[u])?a[u]=n.stats[u]:a[u]=n.stats[u]-T.stats[u],a),{}):n.stats,r={...n,stats:l,races:[],deltaResponses:[]},c={};if("races"in n&&Array.isArray(n.races)){let a=n.races,u=T.races.length?a.slice(T.races.length):a;r.races=u}else r.races=[];if(r.races.length>0){c.count=r.races.length;let a=r.races.map(({delta:h})=>h).filter(h=>!isNaN(h)&&h!==1/0).sort((h,g)=>h-g);c.deltaAvg=a.reduce((h,g)=>h+g,0)/a.length,c.deltaP0=a[0],c.deltaP25=x(a,.25,h=>h),c.deltaP50=x(a,.5,h=>h),c.deltaP75=x(a,.75,h=>h),c.deltaP100=a[a.length-1];let u=r.races.map(({newPathResult:h,oldPathResult:g})=>{let X=(h-g)/g;return X?Math.round((X*100+Number.EPSILON)*100)/100:0}).filter(h=>!isNaN(h)&&h!==1/0).sort((h,g)=>h-g);c.changePercAvg=u.reduce((h,g)=>h+g,0)/u.length,c.changePercP0=u[0],c.changePercP25=x(u,.25,h=>h),c.changePercP50=x(u,.5,h=>h),c.changePercP75=x(u,.75,h=>h),c.changePercP100=u[u.length-1],c.slowerCount=a.filter(h=>h>0).length,c.fasterCount=c.count-c.slowerCount,ne()&&(r.races.forEach(h=>{!h.newPathResult||!h.oldPathResult||O("RACE_RESULT",{raceType:h.raceType||"cnm-fetch-race",raceCondition:e,totalInGroup:r.races.length,deltaChangePercentage:(h.newPathResult-h.oldPathResult)/h.oldPathResult*100,deltaChangeMultiple:h.oldPathResult/h.newPathResult,...h})}),j.log("Races from last view change",r.races))}if("deltaResponses"in n&&Array.isArray(n.deltaResponses)){let a=n.deltaResponses,u=T.deltaResponses.length?a.slice(T.deltaResponses.length):a;r.deltaResponses=u}else r.deltaResponses=[];if(r.deltaResponses.length>0&&(r.deltaResponses.forEach(a=>{O("DELTA_ENCODING_RESULT",{...a})}),j.log("Deltas from last view change",r.deltaResponses)),s){let a={...r,raceResults:c,cnmStatsTrigger:e};delete a.races,delete a.deltaResponses,j.log("Stats from last view change",a),O("CNM_STATS",a)}T=n}var Gn=0,Re;function Lt(){Re&&clearTimeout(Re),Re=setTimeout(()=>{Un(Gn++===0?"page_load":"route_change")},3e3)}function ye(e){document.readyState==="complete"?e():window.addEventListener("load",e)}function Ie(){vt.forEach(e=>e())}var vt=[];ye(function(){window.addEventListener("popstate",Ie);let e=window.history.pushState;window.history.pushState=function(...n){return Ie(),e.apply(window.history,n)};let t=window.history.replaceState;window.history.replaceState=function(...n){return Ie(),t.apply(window.history,n)}});function Mt(e){vt.push(e),e()}var xt=[],Ot=!1,Dt=Date.now();function kt(e){Ot||(window.document.addEventListener("visibilitychange",()=>{let t=Date.now()-Dt;Dt=Date.now(),xt.forEach(n=>n(document.visibilityState==="visible",t))}),Ot=!0),xt.push(e)}var se=E.namespace("destroyer");async function Ae(){let e=p();if("serviceWorker"in navigator&&e?.cnmSWLocation){let t=await navigator.serviceWorker.getRegistrations(),n=new URL(e.cnmSWLocation,location.origin).href,s=t.find(({active:i})=>i&&i.scriptURL===n);if(s)se.log("start destroying sw and artifacts"),d("SELF_DESTRUCT"),setTimeout(()=>{s.unregister().then(i=>{se.log(`sw unregistered itself? ${i?"main thread unregistered":"sw self destroyed"}.`)})},100);else{let i=await caches.keys();i.length>0&&i.find(l=>l.startsWith(v))?await Promise.allSettled([ot(),()=>{self.indexedDB.deleteDatabase(Ge),self.indexedDB.deleteDatabase(Ue),self.indexedDB.deleteDatabase(We)}]).then(l=>{se.log("end destroying sw and artifacts",{results:l})}):se.log("sw or artifacts do not exist, not running destroy fns")}}}qe();var A=E.namespace("MAIN-CLIENT"),Wn=At(p().signal);async function $n(){let e=p();if("serviceWorker"in navigator&&e?.cnmSWLocation){let t=await navigator.serviceWorker.getRegistrations(),n=!1,s=new URL("/",location.origin).href,i=new URL(e.cnmSWLocation,location.origin).href;t.forEach(({scope:o,active:l})=>{o===s&&l&&l.scriptURL!==i&&(n=!0)});try{if(n)return;await navigator.serviceWorker.register(e.cnmSWLocation,{updateViaCache:"none"}),Ht(),Ze({messageHandlers:{SW_ACTIVATION_PROCESS_COMPLETE:()=>Ht(),PING:({payload:o})=>{o?.pongId?d("PONG_"+o.pongId):d("PONG")},GET_PRE_CNM_ASSET_REFS:()=>{ye(()=>{let o=[];performance.getEntriesByType("resource").filter(({name:l})=>{l.startsWith(location.origin)&&!rt(new URL(l,location.origin))&&o.push(l)}),O("CNM_PRE_CNM_RESOURCES",{resourceCount:o.length}),o.length>0?(A.log("Hydrate pre-CNM resources",o),d("HYDRATE_RESOURCES_FROM_HTTP_CACHE",{resources:o})):A.log("no pre-CNM should be hydrated",o)})},HYDRATION_STATS:({payload:o})=>{o&&(A.log("hydrate resource stats",o),O("CNM_HYDRATION_STATS",o))},PRECACHE_STATS:({payload:o})=>{o&&(A.log("precaching stats",o),O("CNM_PRECACHE_STATS",o))},PRECACHE_LOOKAHEADS:Nt,SIGNAL_UPDATED:({payload:o})=>{if(o?.signalKey){let l=o.signalKey,r=o.consistencyVersion||null,c=o.consistencyEnforcement||null;Rt(Wn,p()?.versionControls?.consistencyVersion||"",l,r,c)}}},messageListener:navigator.serviceWorker})}catch(o){A.error(`Registration failed with ${o}`)}}}function Ht(){d("EXPLICIT_ACTIVATE");let e=de();e&&d("TOGGLE_DEBUG",{on:e}),d("UPDATE_CLIENT_SETTINGS",p()),bt()}(async()=>{if(window.__cnmjsInvoked){A.error("client has been loaded multiple times. This script will stop");return}window.__cnmjsInvoked=!0;let e=de();e!==null&&await fe(e);let t=p();if(!t){A.error("settings have not been provided by the snippet. This client will not run");return}window.netlify=window.netlify||{},window.netlify.cnm=window.netlify.cnm||{},window.netlify.cnm.refreshSignal=()=>d("EXPLICIT_SIGNAL_FETCH"),window.netlify.cnm.fetchUrlFromCache=s=>d("FETCH_FROM_CACHE",{url:s}),window.netlify.cnm.precacheResources=s=>te(s,$e),window.netlify.cnm.messageSW=d,window.netlify.cnm.getStats=()=>new Promise(s=>{et("NET_STATS",({payload:i})=>{s(i)}),d("GET_NET_STATS")}),window.netlify.cnm.toggleDebug=()=>{d("TOGGLE_DEBUG"),je()},window.netlify.cnm.destroySW=()=>Ae(),window.netlify.cnm.onDeployChange=s=>{It(s)};let n=!!tt("cnm_sw_enabled")&&M();M()?(A.log("SW is Enabled. Setting value: ",t.clientCaching),$n(),n||nt("cnm_sw_enabled","true")):(A.log("SW is disabled. Setting value: ",t.clientCaching),Ae(),st("cnm_sw_enabled")),kt((s,i)=>{s&&i>2e4&&window.netlify.cnm.refreshSignal()}),Mt(()=>{yt(),Lt(),wt(),window.netlifyCNMReady?.length>0&&(window.netlifyCNMReady.forEach(s=>{try{typeof s=="function"&&s(window.netlify.cnm)}catch(i){console.error(i)}}),window.netlifyCNMReady=[],window.netlifyCNMReady.push=s=>(typeof s=="function"&&setTimeout(()=>{s(window.netlify.cnm)}),-1))}),Y("cnmSWEnabled",M()),Y("cnmSWPreviouslyEnabled",n),Y("cnmNavResourceAffinityEnabled",p().cachingOptions?.navResourceAffinity===ge),Y("cnmDeltaEncoding",p().deltaEncoding||ke)})();})();
