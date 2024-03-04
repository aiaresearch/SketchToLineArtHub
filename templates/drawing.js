// 获取 Canvas 元素和 2D 渲染上下文
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// 获取图片上传输入框元素
const imageInput = document.getElementById('imageInput');

// 监听图片上传输入框的改变事件，并指定处理函数为 handleImageUpload
imageInput.addEventListener('change', handleImageUpload);
//数组
let canvasHistory = [];
let currentIndex = -1;

// 处理图片上传的函数
function handleImageUpload(event) {
    // 获取上传的文件
    const file = event.target.files[0];

    // 检查是否成功获取文件
    if (file) {
        // 创建一个新的 Image 对象来加载图片
        const image = new Image();

        // 使用 URL.createObjectURL() 创建临时 URL，加载图片文件
        image.src = URL.createObjectURL(file);

        //传flask处理
        const formData = new FormData();//定义个表单装图片
        formData.append(image, fileInput.files[0]);//图片加入表单
        fetch('process', {
            method: 'POST',
            body: formData
          })
          .then(response => response.json())
          .then(image => {
            // 使用从后端接收到的图像数据（result）覆盖原来的图像数据（image）
            imageElement.src = image;
          });



        // 当图片加载完成后执行的回调函数
        image.onload = () => {
            // 调整 Canvas 的大小，使其适应图片的宽度和高度
            canvas.width = image.width;
            canvas.height = image.height;

            // 在 Canvas 上绘制加载的图片，坐标为 (0, 0)
            ctx.drawImage(image, 0, 0);
        };
    }
}
