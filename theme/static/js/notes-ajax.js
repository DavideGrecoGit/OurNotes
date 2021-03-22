$(document).ready(function() {
    $('#remove_btn').click(function() {
        if(confirm("Are you sure to delete this group and all its content?")){

            var page = window.location.pathname.split('/')[1]
            var groupIdVar = $(this).attr('data-groupid');

            $.get('/remove_group/', {'group_id': groupIdVar})
            .done( function(){
                
                if(page=="search"){
                    alert("Group deleted with success.\nClick 'OK' to go to the search page");
                    window.location.href = '/search/';
                }else{
                    $("#"+groupIdVar).removeClass("flex");
                    $("#"+groupIdVar).addClass("hidden");
                }
                
            })
            .fail(function(){alert("An error occured while deleting the group");}) 
        }
        
    });
});