function lightbox(e) {//this function displays a larger image positioned on top of the rest fo the page
    "use strict";//Security

    var src = e.src;//get the source of the image that was clicked
    var lighthtml = '<div id="lightbox" onclick="closelightbox()">' +
        '<p>Click to close</p>' +
        '<div id="content">' +
        '<img src="' + src + '" />' +
        '</div>' +
        '</div>';//The Lightbox tags need to show the larger image

    if($('#lightbox').length > 0){//if the lightbox tags already exist in our webpage we don't need to add them again
        $('#content').html('<img src="' + src + '" />');//Set the lightbox img tag the source of the image that was clicked
        $('#lightbox').show();//Show the image

    } else {
        $('#mid_content').append(lighthtml);//if the lightbox html is not in the webpage append to the main content section
    };
};

function closelightbox(){//closes the lightbox
    $('#lightbox').hide();//close the lightbox


};
