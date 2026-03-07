async function uploadPDF(){

    const fileInput = document.getElementById("fileInput")

    if(fileInput.files.length === 0){
        alert("Upload a PDF first")
        return
    }

    const formData = new FormData()
    formData.append("file", fileInput.files[0])

    const res = await fetch("/upload",{
        method:"POST",
        body:formData
    })

    const data = await res.json()

    alert(data.message)

    fileInput.value = ""
}


function addMessage(text,type){

    const chatBox = document.getElementById("chatBox")

    const msg = document.createElement("div")
    msg.classList.add("message")

    if(type === "user"){
        msg.classList.add("user")
    }else{
        msg.classList.add("ai")
    }

    msg.innerText = text

    chatBox.appendChild(msg)

    chatBox.scrollTop = chatBox.scrollHeight
}


async function askQuestion(){

    const input = document.getElementById("question")
    const question = input.value.trim()

    if(question === ""){
        return
    }

    const chatBox = document.getElementById("chatBox")

    // Show user message
    addMessage("You: " + question,"user")

    // Clear the input box
    input.value = ""

    // Show temporary AI message
    const thinking = document.createElement("div")
    thinking.classList.add("message","ai")
    thinking.innerText = "AI is thinking..."
    chatBox.appendChild(thinking)

    const formData = new FormData()
    formData.append("question",question)

    const res = await fetch("/ask",{
        method:"POST",
        body:formData
    })

    const data = await res.json()

    // Remove thinking message
    thinking.remove()

    // Show AI answer
    addMessage("AI: " + data.answer,"ai")
}


// Enter key support
document.getElementById("question").addEventListener("keypress",function(e){

    if(e.key === "Enter"){
        e.preventDefault()
        askQuestion()
    }

})