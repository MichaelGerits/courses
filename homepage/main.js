function ran_col() { //function name
    var color = '#'; // hexadecimal starting symbol
    var letters = ['381D2A','5DB7DE','DB504A','191716','BBD686','CC59D2', 'E71D36', 'B6C649']; //Set your colors here
    var item = document.getElementsByClassName('carousel-item');
    for (var i = 0; i < item.length; i++) {
        color += letters[Math.floor(Math.random() * letters.length)];
        item[i].style.backgroundColor = color;
        color = '#';
    }
}

function getVals() {
    // Selecting the input element and get its value
    let fname = document.getElementById("fname").value;
    let lname = document.getElementById("lname").value;
    let subject = document.getElementById("subject").value;

    document.getElementById("response").innerHTML = `Hello ${fname} ${lname} for your message about ${subject}.`;
}