var canvas;
var ctx;
var rect = {};
var drag = false;
var imageObj = null;

var currentImageIndex = 0;
var rect_tuple = new Array();
//initialize the elements on the body page
function initialize(){

	//initialize the next click button
	nextBtnInit();
	//initialize the back click button
	BackBtnInit();
	//initialize the canvas with image
	canvasInit();
}

function resizeCanvas() {
    canvas.width = imageObj.width;;
    canvas.height = imageObj.height;
}

function getCurrentImageIndex() {
    return images.indexOf(document.getElementById("image").src);
}

function nextBtnInit(){
	$("#next").click(function() 
	{		
		currentImageIndex = parseInt($('#image_index').val())

		nextImage = (currentImageIndex + 1) % images.length;
		currentImageIndex = nextImage;

		ctx.clearRect(0, 0, 400, 400);
		
		//replace the canvas image with the next in array image 
		imageObj = new Image();

		imageObj.onload = function () { 
			resizeCanvas();
			ctx.drawImage(imageObj, 0, 0); };
		

		imageObj.src = '/static/'+images[currentImageIndex];
		
		$('#image_name').val(images[currentImageIndex]);
		$('#image_index').val(currentImageIndex);
		
	});

	$("#btn_viewimg").click(function()
	{
		window.location.href = "/draw/view";
	});

	$("#btn_downloadimg").click(function()
	{
		window.location.href = "/draw/download";
	});

	
}

function BackBtnInit(){
	$("#back").click(function() 
	{		
		currentImageIndex = parseInt($('#image_index').val())
		
		prevImage = (currentImageIndex - 1 + images.length) % images.length;
		currentImageIndex = prevImage;
		ctx.clearRect(0, 0, 400, 400);
		
		//replace the canvas image with the next in array image 
		imageObj = new Image();

		imageObj.onload = function () { 
			resizeCanvas();
			ctx.drawImage(imageObj, 0, 0); };
		

		imageObj.src = '/static/'+images[currentImageIndex];
		
		$('#image_name').val(images[currentImageIndex]);
		$('#image_index').val(currentImageIndex);
		
	});

	$("#btn_viewimg").click(function()
	{
		window.location.href = "/draw/view";
	});

	$("#btn_downloadimg").click(function()
	{
		window.location.href = "/draw/download";
	});

	
}

function clearCanvas() {
	var context = canvas.getContext("2d");
	context.clearRect(0, 0, canvas.width, canvas.height);
	$('#rect_cords').val("");
	rect_tuple = new Array();

	imageObj = new Image();
	imageObj.onload = function () { 
		resizeCanvas();
		ctx.drawImage(imageObj, 0, 0); };

	imageObj.src = '/static/'+images[currentImageIndex];
}

function canvasInit() {
   
	canvas = document.getElementById('canvas');
	ctx = canvas.getContext('2d');

	//event listeners for drawing rectangle
	canvas.addEventListener('mousedown', mouseDown, false);
	canvas.addEventListener('mouseup', mouseUp, false);
	canvas.addEventListener('mousemove', mouseMove, false);

	currentImageIndex = parseInt($('#image_index').val())
	

	imageObj = new Image();
	imageObj.onload = function () { 
		resizeCanvas();
		ctx.drawImage(imageObj, 0, 0); };
	imageObj.src = '/static/'+images[currentImageIndex];
	
	//add the image name to the form for saving to file
	$('#image_name').val(images[currentImageIndex]);
	
}




function mouseDown(e) {

	// since the canvas is moved form the center
	// the drawing coordinates need to be adjusted
	// accoding to the offset moved
	var windowTop = $(window).scrollTop();
	var windowLeft = $(window).scrollLeft();

	var canvasTop =  $('#canvas').offset().top;
	var canvasLeft = $('#canvas').offset().left;

	var offsetTopAdd = canvasTop - windowTop;
	var offsetLeftAdd = canvasLeft - windowLeft;
	
	rect.startX = e.pageX - (this.offsetLeft+offsetLeftAdd);
	rect.startY = e.pageY - (this.offsetTop+offsetTopAdd);

	drag = true;
}

function mouseUp(e) { 

	// We need to store the top-left coordinate of the bounding box.
	// In order to do that, we need to figure out from which direction
	// has the user drawn the rectangle (whether from bottom left -> top right...)
	// Therefore; based on the set of conditions we swap the ending 
	// and starting points

	var windowTop = $(window).scrollTop();
	var windowLeft = $(window).scrollLeft();

	var canvasTop =  $('#canvas').offset().top;
	var canvasLeft = $('#canvas').offset().left;

	var offsetTopAdd = canvasTop - windowTop;
	var offsetLeftAdd = canvasLeft - windowLeft;

	rect.endingX = e.pageX - (this.offsetLeft);
	rect.endingY = e.pageY - (this.offsetTop);

	
	if((rect.startX > rect.endingX) && (rect.startY > rect.endingY))
	{
		rect.startX = rect.endingX;
		rect.startY = rect.endingY;
	}
	else if((rect.startX < rect.endingX) && (rect.startY < rect.endingY))
	{
		rect.startX = rect.startX;
		rect.startY = rect.startY;
	}
	else if((rect.startX < rect.endingX) && (rect.startY > rect.endingY))
	{
		var height = (e.pageY - this.offsetTop) - (rect.endingY+offsetTopAdd);
		rect.startY = rect.startY + height;
	}
	else if((rect.startX > rect.endingX) && (rect.startY < rect.endingY))
	{
		var width = (e.pageX - this.offsetLeft) - (rect.endingX+offsetLeftAdd);
		rect.startX = rect.startX + width;
	}

	
	var tempRectTuple = []
	// top-left
	tempRectTuple.push(rect.startX);
	tempRectTuple.push(rect.startY);
	//bottom-right
	tempRectTuple.push((rect.startX + Math.abs(rect.w)));
	tempRectTuple.push((rect.startY + Math.abs(rect.h)));
	//width
	tempRectTuple.push(Math.abs(rect.w));
	//height
	tempRectTuple.push(Math.abs(rect.h));

	var tempStr = "["+tempRectTuple+"]";
	rect_tuple.push(tempRectTuple)
 

	 $('#rect_cords').val(rect_tuple)
	//add the rectangle dimensions to the form for saving to file
	drag = false; 

}

function mouseMove(e) {
	if (drag) {
		//ctx.moveTo(canvas.offsetWidth,canvas.offsetHeight)
		ctx.drawImage(imageObj, 0, 0);

		var windowTop = $(window).scrollTop();
		var windowLeft = $(window).scrollLeft();

		var canvasTop =  $('#canvas').offset().top;
		var canvasLeft = $('#canvas').offset().left;

		var offsetTopAdd = canvasTop - windowTop;
		var offsetLeftAdd = canvasLeft - windowLeft;

		//start drawing liens for the rectanle
		rect.w = (e.pageX - this.offsetLeft) - (rect.startX+offsetLeftAdd);
		rect.h = (e.pageY - this.offsetTop) - (rect.startY+offsetTopAdd);
		ctx.strokeStyle = 'red';
		ctx.strokeRect(rect.startX, rect.startY, rect.w, rect.h);
	}
}
