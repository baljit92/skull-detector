var canvas;
var ctx;
var rect = {};
var drag = false;
var imageObj = null;
var images = [];
var currentImageIndex = 0;

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
	nextBtnInit()

	//initialize the canvas with image
	canvasInit()
}

function nextBtnInit(){
	$("#next").click(function() 
	{
		if(currentImageIndex < images.length-1){
			currentImageIndex += 1;  
		}
		else{
			currentImageIndex = 0;
		}
		
		ctx.clearRect(0, 0, 400, 400);
		
		//replace the canvas image with the next in array image 
		imageObj = new Image();
		imageObj.onload = function () { ctx.drawImage(imageObj, 0, 0, 400, 400); };
		imageObj.src = '/static/'+images[currentImageIndex];

	});
}


function canvasInit() {
   
	canvas = document.getElementById('canvas');
	ctx = canvas.getContext('2d');

	//event listeners for drawing rectangle
	canvas.addEventListener('mousedown', mouseDown, false);
	canvas.addEventListener('mouseup', mouseUp, false);
	canvas.addEventListener('mousemove', mouseMove, false);

	imageObj = new Image();
	imageObj.onload = function () { ctx.drawImage(imageObj, 0, 0, 400, 400); };
	imageObj.src = '/static/'+images[0];
}

function mouseDown(e) {
	rect.startX = e.pageX - this.offsetLeft;
	rect.startY = e.pageY - this.offsetTop;
	drag = true;
}

function mouseUp() { drag = false; }

function mouseMove(e) {
	if (drag) {

		//clear out any existing rectangles on the canvas
		ctx.clearRect(0, 0, 400, 400);

		ctx.drawImage(imageObj, 0, 0, 400, 400);

		//start drawing liens for the rectanle
		rect.w = (e.pageX - this.offsetLeft) - rect.startX;
		rect.h = (e.pageY - this.offsetTop) - rect.startY;
		ctx.strokeStyle = 'red';
		ctx.strokeRect(rect.startX, rect.startY, rect.w, rect.h);
	}
}



function save_canvas(url) {
	$.get('upload_pic/'+images[currentImageIndex]+'/', function (data) {
		alert("Image name:", images[currentImageIndex]);
	});
}

