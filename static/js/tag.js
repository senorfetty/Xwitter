function tagTag() {
    const element= document.getElementsByClassName('b')

    for (let i=0;i<element.length;i++) {
        let txt= element[i].children[0].innerHTML

        let word= txt.split(" ");

        for (let j=0;j < word.length;j++) {
            if (word[j][0]  === '#') {
                let newWord= txt.replace(/\s\#(.*?)(\s|$)/g, ` <a href='#'>${word[j]}</a>`)
                element[i].innerHTML = newWord
            }
        }

    }
}