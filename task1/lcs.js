console.log((([,,x='',...a])=>{
    e=l=x.length;
    for(;l>=0;l--)
        for(y=0;y<=e-l;y++)
            if(s=x.substr(y,l),a.every(t=>t.includes(s)))
                return s
})(process.argv))