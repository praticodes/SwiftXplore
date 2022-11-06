localStorage.removeItem('locations')
var array= document.getElementsByClassName("btn-dark")
var List_of_places=[]
var count=0
for(let i=0;i<15;i++){
        array[i].addEventListener("click",function () {
        if(List_of_places.includes(this.id)){alert("You have already selected this location.")}
        else{List_of_places.push(this.id)
        count+=1
        document.getElementById("counter").innerHTML="Locations selected so far: "+List_of_places.toString();
      localStorage.setItem('locations', List_of_places)
}})
}
