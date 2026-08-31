const AT={
  mount(selector,path){const el=document.querySelector(selector);if(!el)return fetch(path).then(r=>r.ok?r.text():Promise.reject(r.status)).then(html=>{el.innerHTML=html}).catch(()=>{});return fetch(path).then(r=>r.text()).then(html=>{el.innerHTML=html}).catch(()=>{})},
  async init(){await Promise.all([this.mount('[data-header]','/components/header.html'),this.mount('[data-nav]','/components/navigation.html'),this.mount('[data-footer]','/components/footer.html'),this.mount('[data-back-top]','/components/back-to-top.html')]);this.initNav();this.initBackTop();this.markActive() },
  initNav(){const toggle=document.querySelector('[data-menu-toggle]'),nav=document.querySelector('[data-site-nav]');if(toggle&&nav)toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open))})},
  initBackTop(){const b=document.querySelector('[data-back-top]');if(!b)return;const sync=()=>b.classList.toggle('show',window.scrollY>450);window.addEventListener('scroll',sync,{passive:true});b.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));sync()},
  markActive(){const current=location.pathname.replace(/\/$/,'')||'/';document.querySelectorAll('.site-nav a').forEach(a=>{const href=new URL(a.href).pathname.replace(/\/$/,'')||'/';if(href===current)a.classList.add('active')})}
};
document.addEventListener('DOMContentLoaded',()=>AT.init());
