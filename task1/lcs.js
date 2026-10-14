[,,x='',...a]=process.argv;
e=l=x.length;
o:for(;l>=0;l--)
    for(y=0;y<=e-l;y++)
        if(s=x.substr(y,l),a.every(t=>t.includes(s)))
            break o;
console.log(s)