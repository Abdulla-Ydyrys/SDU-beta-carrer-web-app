$(document).ready(function () {                      //run when the DOM is ready
          $(".profile_btn").click(function() {  //use a class, since your ID gets mangled
            $('.MuiModal-root').removeClass("css-1t7fjoj-MuiModal-root");      //add the class to the clicked element
          });
          $('.MuiModal-root').click(function(e) {
            var clicked = $(e.target);

            if (!clicked.hasClass('MuiPaper-root')) {
              if (!clicked.parents().hasClass('MuiPaper-root')) {
                $('.MuiModal-root').addClass("css-1t7fjoj-MuiModal-root");  
              }
            }
          })

    const actualBtn = document.getElementById('actual-btn');

    const fileChosen = document.getElementById('file-chosen');

    actualBtn.addEventListener('change', function(){
    fileChosen.textContent = this.files[0].name
    })
});


