function changeType (myStuffs) {
    var input,butt,ch,i;
    butt = document.getElementById('changeIcon');
    ch = document.getElementById('changes');
    for (i=0; i<myStuffs.length ; i++) {
        input = document.getElementById(myStuffs[i]);
        input.type = (input.type === "password")?"text":"password";
    }
    if (input.type == "text") {
        ch.textContent = "Hide Password";
        butt.classList.add("fa-eye-slash");
        butt.classList.remove("fa-eye");
    }
    else {
        ch.textContent = "Show Password";
        butt.classList.add("fa-eye");
        butt.classList.remove("fa-eye-slash");
    }
}

function setTime () {
    r = document.getElementById("greet");
    s = document.getElementById("times");
    e = new Date();
    h = e.getHours();
    M = e.getMinutes();
    S = e.getSeconds();

    if (h >= 0 && h < 12)
        r.textContent = "Morning";
    else if (h >= 12 && h < 17)
        r.textContent = "Afternoon";
    else    
        r.textContent = "Evening";

    m = (h >= 12)?"PM":"AM";
    h = (h > 12)?(h-12):(h == 0)?12:h;

    s.textContent = `${(h < 10)?('0'+h):h}:${(M < 10)?('0'+M):M}:${(S < 10)?('0'+S):S} ${(h >= 12)?"PM":"AM"}`;

    setInterval (myTime,1000);

    function myTime () {
        e = new Date();
        h = e.getHours();
        M = e.getMinutes();
        S = e.getSeconds();

        h = (h > 12)?(h-12):(h == 0)?12:h;
        s.textContent = `${(h < 10)?('0'+h):h}:${(M < 10)?('0'+M):M}:${(S < 10)?('0'+S):S} ${(h >= 12)?"PM":"AM"}`;
    }

}