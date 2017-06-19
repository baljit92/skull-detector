var canvas;
var ctx;
var rect = {};
var drag = false;
var imageObj = null;
var images = [];
var currentImageIndex = 0;
var rect_tuple = new Array();
//initialize the elements on the body page
function initialize(){

	//push images from the folder to an array for indexing
	for(var i=1;i<52;i++)
	{
		if(i<10)
			images.push("media/skull00"+i+".jpg");
		else if(i<100 && i>=10)
			images.push("media/skull0"+i+".jpg");
		else
			images.push("media/skull"+i+".jpg");
	}
	//initialize the next clicl button
	nextBtnInit();
	//initialize the canvas with image
	canvasInit();
}

function nextBtnInit(){
	$("#next").click(function() 
	{	
		currentImageIndex = parseInt($('#image_index').val())

		if(currentImageIndex < images.length-1){
			currentImageIndex += 1;  
		}
		else{
			currentImageIndex = 0;
		}
		
		ctx.clearRect(0, 0, 400, 400);
		
		//replace the canvas image with the next in array image 
		imageObj = new Image();

		imageObj.onload = function () { ctx.drawImage(imageObj, 0, 0); };
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

function canvasInit() {
   
	canvas = document.getElementById('canvas');
	ctx = canvas.getContext('2d');

	//event listeners for drawing rectangle
	canvas.addEventListener('mousedown', mouseDown, false);
	canvas.addEventListener('mouseup', mouseUp, false);
	canvas.addEventListener('mousemove', mouseMove, false);

	currentImageIndex = parseInt($('#image_index').val())
	

	imageObj = new Image();
	imageObj.onload = function () { ctx.drawImage(imageObj, 0, 0); };
	imageObj.src = '/static/'+images[currentImageIndex];
	//add the image name to the form for saving to file
	$('#image_name').val(images[currentImageIndex]);
	
}

function mouseDown(e) {
	rect.startX = e.pageX - this.offsetLeft;
	rect.startY = e.pageY - this.offsetTop;

	drag = true;
}

function Shape(x1, y1, x2, y2, w, h) {
    this.x1 = x1;
    this.y1 = y1;
    this.x2 = x2;
    this.y2 = y2;
    this.w = w;
    this.h = h;
    
}

function mouseUp(e) { 

	rect.endingX = e.pageX - this.offsetLeft;
	rect.endingY = e.pageY - this.offsetTop
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
		var height = (e.pageY - this.offsetTop) - rect.startY
		rect.startY = rect.startY + height;
	}
	else if((rect.startX > rect.endingX) && (rect.startY < rect.endingY))
	{
		var width = (e.pageX - this.offsetLeft) - rect.startX
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

		//clear out any existing rectangles on the canvas
		//ctx.clearRect(0, 0, 400, 400);

		ctx.drawImage(imageObj, 0, 0);

		//start drawing liens for the rectanle
		rect.w = (e.pageX - this.offsetLeft) - rect.startX;
		rect.h = (e.pageY - this.offsetTop) - rect.startY;
		ctx.strokeStyle = 'red';
		ctx.strokeRect(rect.startX, rect.startY, rect.w, rect.h);

		// var tempRect = rect.startX+","+rect.startY+","+Math.abs(rect.w)+","+Math.abs(rect.h);
		// //add the rectangle dimensions to the form for saving to file
		// $('#rect_cords').val(tempRect)
	}
}
