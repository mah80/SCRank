
document.addEventListener('click', function (event) {
// document.getElementById('submit_url').addEventListener('click', function() {
    // Handle click event
    var element = event.target;
    console.log(element.id == "submit_url");
    if (element.id == "submit_url"){
        element.disabled = true;
        element.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                 <span class="">Processing...</span>`;
        
        document.getElementById("submit_repo").disabled = true;
        document.getElementById("zip_form").submit();
        
    }
    else if (element.id == "submit_repo"){
        element.disabled = true;
        element.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                                 <span class="">Processing...</span>`;
        
        document.getElementById("submit_url").disabled = true;
        document.getElementById("git_form").submit();
    }
    // const urlButton = document.getElementById('submit_url')
    // console.log('Button clicked!');
    // urlButton.disabled = true;
    // urlButton.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
    //                         <span class="">Processing...</span>`;

    // Other logic like making API call 
});
