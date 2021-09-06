console.log(`Loaded`)

populateBtn = document.getElementById("populate-sgid");
populateBtn2 = document.getElementById("populate-idw");

populateBtn.onclick = function(){ 
    const url = populateBtn.getAttribute('url')
    populate(url) 
}
populateBtn2.onclick = function(){ 
    const url = populateBtn2.getAttribute('url')
    populate(url) 
 }


async function populate(url) {
    console.log(`requesting ${url}`)
    res = await fetch(url)
    console.log(`res.status`, res.status)
}