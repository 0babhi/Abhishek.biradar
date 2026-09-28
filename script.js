const menuBtn=document.querySelector('.menu-btn');
const nav=document.querySelector('.nav');
if(menuBtn) menuBtn.addEventListener('click',()=>nav.classList.toggle('open'));

const filters=document.querySelectorAll('.filter');
const projects=document.querySelectorAll('.project');
filters.forEach(btn=>{
  btn.addEventListener('click',()=>{
    filters.forEach(x=>x.classList.remove('active'));
    btn.classList.add('active');
    const filter=btn.dataset.filter;
    projects.forEach(card=>{
      const tags=card.dataset.tags || '';
      card.style.display=(filter==='all'||tags.includes(filter))?'flex':'none';
    });
  });
});
