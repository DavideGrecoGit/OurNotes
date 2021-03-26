function manage_member(btn, view_name, remove_group=false){
    var page = window.location.pathname.split('/')[1]
    var group_slug = $(btn).attr('data-group_slug');

    $.get('/'+view_name+'/', {'group_slug': group_slug})
    .done( function(){
        
        if(page=="search"){
            // If Page does not exist anymore, redirect to search
            if(remove_group){
                alert("Group deleted with success.\nClick 'OK' to go to the search page");
                window.location.href = '/search/';
            }
            //Else reload
            else{
                location.reload();
            }
            
        }else{
            // No need to reload
            $("#"+group_slug).removeClass("flex");
            $("#"+group_slug).addClass("hidden");
        }
    })
    .fail(function(){alert("An error occured");})
}

$(document).ready(function() {
    $('#remove_btn').click(function() {
        if(confirm("Are you sure to delete this group and all its content?")){
            manage_member(this, 'remove_group', remove_group=true)
        }
    });

    $('#leave_btn').click(function() {
        manage_member(this, 'remove_group')
    });

    $('#join_btn').click(function() {
        manage_member(this, 'join_group')
    });

    $(".remove_note_btn").click(function() {
        if(confirm("Are you sure to remove this note?")){
            var note_id = $(this).attr('data-note_id');

            $.get('/remove_note/', {'note_id': note_id})
            .done( function(){
                // No need to reload
                $("#"+note_id).removeClass("flex");
                $("#"+note_id).addClass("hidden");
            })
            .fail(function(){alert("An error occured");})
        }
    });

    $('.vote_btn').click(function() {

        var comment_id = $(this).attr('data-comment_id');
        var vote = $(this).attr('data-vote');
        
        var upVote = $("#"+comment_id).find('.upVote');
        var downVote = $("#"+comment_id).find('.downVote');

        if(vote==1 && upVote.attr('src') == "/static/icons/upVote.png" ){
            return
        }

        if(vote==0 && downVote.attr('src') == "/static/icons/downVote.png"){
            return
        }

        $.get('/vote_comment/', {'comment_id': comment_id,'vote':vote})
        .done( function(votes){
            // No need to reload
            
            // Change vote numbers
            $("#"+comment_id).find('#upVotes').html( votes['upVotes'] );
            $("#"+comment_id).find('#downVotes').html( votes['downVotes'] );

            // Change vote Icons
            if (vote == "1" && upVote.attr('src') == "/static/icons/upVote_empty.png") {
                upVote.attr('src', '/static/icons/upVote.png');
            }
            if (vote == "0" && upVote.attr('src') == "/static/icons/upVote.png") {
                upVote.attr('src', '/static/icons/upVote_empty.png');
            }
            
            if (vote == "1" && downVote.attr('src') == "/static/icons/downVote.png") {
                downVote.attr('src', '/static/icons/downVote_empty.png');
            } 
            if (vote == "0" && downVote.attr('src') == "/static/icons/downVote_empty.png") {
                downVote.attr('src', '/static/icons/downVote.png');
            } 
        })
        .fail(function(){alert("An error occured");})
    });
});
